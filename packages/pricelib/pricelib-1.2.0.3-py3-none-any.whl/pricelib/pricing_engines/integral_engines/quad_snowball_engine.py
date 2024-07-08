#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C) 2024 Galaxy Technologies
Licensed under the Apache License, Version 2.0
"""
import numpy as np
from pricelib.common.utilities.enums import StatusType, QuadMethod
from pricelib.common.pricing_engine_base import QuadEngine
from pricelib.common.time import global_evaluation_date


class QuadSnowballEngine(QuadEngine):
    """雪球数值积分法定价引擎
    只支持不是仅到期观察敲入的结构 (只有到期观察敲入的结构，如FCN、DCN等另有更快的算法)
    支持变敲出、变敲入、变票息等要素可变型雪球结构"""

    def __init__(self, stoch_process=None, quad_method=QuadMethod.Simpson, n_points=1301, *,
                 s=None, r=None, q=None, vol=None):
        """初始化数值积分法定价引擎
        Args:
            stoch_process: StochProcessBase，随机过程
            quad_method: 数值积分方法，QuadMethod枚举类，Trapezoid梯形法则/Simpson辛普森法则
            n_points: int，积分点个数 (需要注意，辛普森法则的n_points必须是奇数)
        在未设置stoch_process时，(stoch_process=None)，会默认创建BSMprocess，需要输入以下变量进行初始化
            s: float，标的价格
            r: float，无风险利率
            q: float，分红/融券率
            vol: float，波动率
        """
        super().__init__(stoch_process, quad_method, n_points, s=s, r=r, q=q, vol=vol)
        # 以下为计算过程的中间变量
        self.prod = None  # Product产品对象
        self.obs_dates = None  # 根据估值日，将敲出观察日转化为List[int]，交易日期限
        self.pay_dates = None  # 根据估值日，将支付日转化为List[float]，年化自然日期限
        self.diff_obs_pay_dates = None  # 观察日与付息日的差值，List[float]，年化自然日期限
        self.smax = None  # 价格网格上界，float
        self.smin = None  # 价格网格下界，float
        self.s_vec = None  # 价格格点(不含smax和smin)，np.ndarray
        self.dt = None  # 时间步长，float
        self.j_vec = None  # 时间格点向量，np.ndarray
        self.v_not_in = None  # 未敲入时的期权价值矩阵，np.ndarray
        self.v_knock_in = None  # 敲入时的期权价值矩阵，np.ndarray
        self.next_paydate = None
        self.out_dates = None  # 逆序敲出观察日，List[int]，交易日期限
        self.next_diff_obspaydate = None  # 每个交易日对应的下一个敲出观察日对应的付息日与观察日的自然日年化之差
        self.next_barrier_out = None
        self.next_barrier_in = None
        self.out_idxs = None
        self.in_idx = None
        self.itm = None
        self.next_coupon_out = None
        self.reversed_barrier_out = None
        self.reversed_barrier_in = None
        self.reversed_coupon_out = None
        self.coupon_outs = None
        self._barrier_in = None  # 是经过估值日截断之后的列表，例如prod.barrier_in有22个，存续一年时估值，self._barrier_in只有12个
        self._barrier_out = None  # 是经过估值日截断之后的列表，例如prod.barrier_out有22个，存续一年时估值，self._barrier_out只有12个
        self._coupon_out = None  # 是经过估值日截断之后的列表，例如prod.coupon_out有22个，存续一年时估值，self._coupon_out只有12个

    # pylint: disable=too-many-locals, too-many-statements
    def calc_present_value(self, prod, t=None, spot=None):
        """计算现值
        Args:
            prod: Product产品对象
            t: datetime.date，估值日; 如果是None，则使用全局估值日globalEvaluationDate
            spot: float，估值日标的价格，如果是None，则使用随机过程的当前价格
        Returns: float，现值
        """
        self.prod = prod
        calculate_date = global_evaluation_date() if t is None else t
        _maturity = (prod.end_date - calculate_date).days / prod.annual_days.value
        self.backward_steps = prod.trade_calendar.business_days_between(calculate_date, prod.end_date)
        obs_dates = prod.obs_dates.count_business_days(calculate_date)
        obs_dates = np.array([num for num in obs_dates if num >= 0])
        calculate_start_diff = (calculate_date - prod.start_date).days
        pay_dates = prod.pay_dates.count_calendar_days(prod.start_date)
        self.pay_dates = np.array([num / prod.annual_days.value for num in pay_dates if num >= calculate_start_diff])
        assert len(obs_dates) == len(self.pay_dates), f"Error: {prod}的观察日和付息日长度不一致"
        self.diff_obs_pay_dates = np.array([(prod.pay_dates.date_schedule[i] - prod.obs_dates.date_schedule[i]).days
                                            for i in range(len(obs_dates))]) / prod.annual_days.value
        if spot is None:
            spot = self.process.spot()
        r = self.process.interest(_maturity)
        q = self.process.div(_maturity)
        vol = self.process.vol(_maturity, spot)
        self._check_method_params()
        self.set_quad_params(r=r, q=q, vol=vol)
        # 初始化fft的对数价格向量及边界的对数价格向量
        self.init_grid(spot, vol, self.backward_steps / prod.t_step_per_year)

        self.s_vec = np.exp(self.ln_s_vec)
        self.dt = 1 / prod.t_step_per_year
        self.j_vec = np.linspace(0, self.backward_steps, self.backward_steps + 1)  # 生成时间格点
        self.v_not_in = np.zeros(shape=(self.n_points, self.backward_steps + 1))
        self.v_knock_in = np.zeros(shape=(self.n_points, self.backward_steps + 1))

        # 初始化逆序敲出观察日
        if isinstance(obs_dates, (list, np.ndarray)):  # 敲出观察日是具体第n天数的列表，如[11,22,32,43,53,64]
            self.out_dates = np.round(np.flip(np.array(obs_dates))).astype(int)
        elif isinstance(obs_dates, (int, np.int32)):  # 敲出观察日是整数， 敲出观察日个数，如6代表6个均匀分布的观察日
            out_dates = (self.backward_steps - np.round(np.linspace(0, self.backward_steps,
                                                                    round(obs_dates + 1)))[:-1])
            self.out_dates = out_dates.astype(int)
        else:
            raise ValueError('敲出观察日类型设置错误，请检查')
        self.next_diff_obspaydate = self.diff_obs_pay_dates.repeat(
            np.diff(np.append(np.zeros((1,)), self.out_dates[::-1])).astype(int))  # 计息时间数
        self.next_diff_obspaydate = np.append(self.diff_obs_pay_dates[0],
                                              self.next_diff_obspaydate)  # 每个交易日对应的下一个敲出观察日对应的付息日与观察日的自然日年化之差
        # 初始化票息支付日
        self.next_paydate = self.pay_dates.repeat(
            np.diff(np.append(np.zeros((1,)), self.out_dates[::-1])).astype(int))  # 计息时间数
        self.next_paydate = np.append(self.pay_dates[0], self.next_paydate)  # 每个交易日对应的下一个敲出观察日对应的付息日

        # 设置期末价值状态
        self._init_terminal_condition(self.s_vec)

        if self.backward_steps == 0:  # 如果估值日是到期日
            if prod.status == StatusType.DownTouch:  # 已敲入
                return self.v_knock_in[0, 0]
            else:   # 未敲入
                return self.v_not_in[0, 0]

        if 0 in self.out_dates:
            # 如果估值日就是敲出观察日
            j = 0
            # 如果敲出价是浮动的，调整敲出价
            start_barrier_out = (self.reversed_barrier_out[np.where(self.out_dates == j)[0][0]]
                                     if isinstance(prod.barrier_out, (list, np.ndarray)) else prod.barrier_out)
            if spot >= start_barrier_out:  # 发生敲出
                # 如果敲出票息是浮动的，调整敲出票息
                start_coupon_out = (self.reversed_coupon_out[np.where(self.out_dates == j)[0][0]]
                                        if isinstance(prod.coupon_out, (list, np.ndarray)) else prod.coupon_out)
                start_t = 1 if prod.trigger else self.next_paydate[j]
                return np.where(spot - prod.strike_call > 0, (spot - prod.strike_call) * prod.parti_out, 0) + (
                        prod.margin_lvl + start_coupon_out * start_t) * prod.s0 * self.process.interest.disc_factor(
                    self.next_paydate[j], self.next_paydate[j] - self.next_diff_obspaydate[j])

        for j in range(self.backward_steps - 1, 0, -1):
            # 未敲入网格更新
            if prod.status == StatusType.NoTouch:
                self.v_not_in[:, j] = self.fft_step_backward(self.ln_s_vec, self.ln_s_vec,
                                                             self.v_not_in[:, j + 1], self.dt)
            # 已敲入网格更新
            self.v_knock_in[:, j] = self.fft_step_backward(self.ln_s_vec, self.ln_s_vec,
                                                           self.v_knock_in[:, j + 1], self.dt)

            if j in self.out_dates:
                coupon_t = 1 if prod.trigger else self.next_paydate[j]
                # 如果敲出价是浮动的，调整敲出价
                self.next_barrier_out = (self.reversed_barrier_out[np.where(self.out_dates == j)[0][0]]
                                         if isinstance(prod.barrier_out, (list, np.ndarray)) else prod.barrier_out)
                self.out_idxs = np.array(np.where(self.s_vec >= self.next_barrier_out)[0])
                # 如果敲出票息是浮动的，调整敲出票息
                self.next_coupon_out = (self.reversed_coupon_out[np.where(self.out_dates == j)[0][0]]
                                        if isinstance(prod.coupon_out, (list, np.ndarray)) else prod.coupon_out)
                # 发生敲出的payoff
                knock_out_payoff = self.itm[self.out_idxs] + (
                    prod.margin_lvl + self.next_coupon_out * coupon_t) * prod.s0 * self.process.interest.disc_factor(
                    self.next_paydate[j], self.next_paydate[j] - self.next_diff_obspaydate[j])
                # 用knock_out_payoff覆盖敲出价上方的衍生品价值
                self.v_not_in[self.out_idxs, j] = self.v_knock_in[self.out_idxs, j] = knock_out_payoff

                # 如果敲入价是浮动的，调整敲入价
                self.next_barrier_in = self.reversed_barrier_in[np.where(self.out_dates == j)[0][0]] if isinstance(
                    prod.barrier_in, (list, np.ndarray)) else prod.barrier_in
                if self.next_barrier_in > 0 and self.s_vec[0] <= self.next_barrier_in:
                    self.in_idx = np.where(self.s_vec <= self.next_barrier_in)[0][-1]
                else:
                    self.in_idx = 0

            if prod.status == StatusType.NoTouch:
                # 未敲入网格-敲入线下方的价值等于已敲入网格
                self.v_not_in[:self.in_idx, j] = self.v_knock_in[:self.in_idx, j]

        x = np.array([np.log(spot)])
        if prod.status == StatusType.NoTouch and spot > self.next_barrier_in:
            value = self.fft_step_backward(x, self.ln_s_vec, self.v_not_in[:, 1], self.dt)[0]
        else:
            value = self.fft_step_backward(x, self.ln_s_vec, self.v_knock_in[:, 1], self.dt)[0]
        return value

    def _init_terminal_condition(self, s_vec):
        """初始化终止时已敲入且未敲出、未敲入且未敲出的期权价值
        Args:
            s_vec: List[float], 网格的价格格点
            maturity: float, 到期时间，年化自然日期限
        Returns: None
        """
        prod = self.prod
        # 初始化next_barrier_in、next_barrier_out、next_coupon_out为最后一期的敲入价、敲出价、敲出票息。若变敲出变敲入，需要动态调整
        # 设置到期日的敲入边界位置
        if isinstance(prod.barrier_in, (int, float, np.int32, np.float64)):
            # 常数敲入雪球
            self.next_barrier_in = prod.barrier_in
        elif isinstance(prod.barrier_in, (list, np.ndarray)):
            # self.out_dates是估值日之后的、经过截断的敲出观察日，取产品参数列表中最后len(self.out_dates)个，与其对应
            self._barrier_in = prod.barrier_in[-len(self.out_dates):].copy()
            # 浮动敲入雪球
            self.next_barrier_in = self._barrier_in[-1]
            self.reversed_barrier_in = np.flip(np.array(self._barrier_in))
        else:
            raise ValueError(f'敲入障碍价类型为{type(prod.barrier_in)}，仅支持int/float/list/np.ndarray，请检查')

        # 设置到期日的敲出边界位置
        if isinstance(prod.barrier_out, (int, float, np.int32, np.float64)):
            # 常数敲出雪球
            self.next_barrier_out = prod.barrier_out
        elif isinstance(prod.barrier_out, (list, np.ndarray)):
            # self.out_dates是估值日之后的、经过截断的敲出观察日，取产品参数列表中最后len(self.out_dates)个，与其对应
            self._barrier_out = prod.barrier_out[-len(self.out_dates):].copy()
            # 阶梯式雪球
            self.next_barrier_out = self._barrier_out[-1]
            self.reversed_barrier_out = np.flip(np.array(self._barrier_out))
        else:
            raise ValueError(f'敲出障碍价类型为{type(prod.barrier_out)}，仅支持int/float/list/np.ndarray，请检查')

        # 敲出票息
        if isinstance(prod.coupon_out, (int, float, np.int32, np.float64)):
            # 常数敲出票息
            self.next_coupon_out = prod.coupon_out
            # N天的敲出票息列表，用于生成mspot价格上边界条件
            self.coupon_outs = np.full(self.backward_steps + 1, prod.coupon_out)
        elif isinstance(prod.coupon_out, (list, np.ndarray)):
            # self.out_dates是估值日之后的、经过截断的敲出观察日，取产品参数列表中最后len(self.out_dates)个，与其对应
            self._coupon_out = prod.coupon_out[-len(self.out_dates):].copy()
            # 浮动敲出票息
            self.next_coupon_out = self._coupon_out[-1]
            self.reversed_coupon_out = np.flip(np.array(self._coupon_out))
            # N天的敲出票息列表，用于生成smax价格上边界条件
            coupon_outs = np.array(self._coupon_out).repeat(
                np.diff(np.append(np.zeros((1,)), self.out_dates[::-1])).astype(int))
            self.coupon_outs = np.append(self._coupon_out[0], coupon_outs)
        else:
            raise ValueError(f'敲出票息类型为{type(prod.coupon_out)}，仅支持int/float/list/np.ndarray，请检查')

        # in_idx：小于到期日敲入线的最大的标的价格索引。如果是变敲入雪球，此变量in_idx应该随敲入价动态调整。
        if self.next_barrier_in > 0 and s_vec[0] <= self.next_barrier_in:
            self.in_idx = np.where(s_vec <= self.next_barrier_in)[0][-1]
        else:
            self.in_idx = 0
        # out_idxs：大于到期日敲出线的标的价格数组的索引。如果是变敲出雪球，此变量out_idxs应该随敲出价动态调整。
        self.out_idxs = np.array(np.where(s_vec >= self.next_barrier_out)[0])
        # 虚值call在值度
        self.itm = np.where(s_vec - prod.strike_call > 0, (s_vec - prod.strike_call) * prod.parti_out, 0)

        coupon_t = 1 if prod.trigger else self.pay_dates[-1]  # 票息是否年化
        # 矩阵最后一列：到期payoff。考虑到了保底、保证金\纯期权模式、以及敲出边界上方增加虚值call
        """已敲入：如果到期小于敲出边界，在100%本金模式下，小于保底边界，获得保底价；
                                                  大于保底边界，获得到期价格；
                                   在保证金模式下，小于保底边界，支付期初价（高行权价）与保底价之间价差；
                                                  大于保底边界，支付到期价格与期初价之间价差；
                  如果到期大于敲出边界，大于看涨行权价，获得看涨收益、本金和票息；
                                    在敲出边界和看涨行权价之间，获得本金和票息"""
        self.v_knock_in[:, -1] = np.where(s_vec < self.next_barrier_out,
                                          np.minimum(np.where(s_vec <= prod.strike_lower, prod.strike_lower, s_vec) -
                                                     prod.strike_upper, 0)
                                          + prod.s0 * prod.margin_lvl,
                                          np.where(s_vec > prod.strike_call,
                                                   (s_vec - prod.strike_call) * prod.parti_out + (
                                                        prod.margin_lvl + self.next_coupon_out * coupon_t) * prod.s0,
                                                   (prod.margin_lvl + self.next_coupon_out * coupon_t) * prod.s0))
        """未敲入：如果到期小于敲入边界，在100%本金模式下，小于保底边界，获得保底价；
                                                  大于保底边界，获得实际价格；
                                  在保证金模式下，小于保底边界，支付保底价与期初价之间价差；
                                                  大于保底边界，支付到期价格与期初价之间价差；
                 如果到期大于敲入边界，且大于看涨行权价，获得看涨收益、本金和票息；
                                  在敲入边界和看涨行权价之间，获得本金和票息
                                          如果在敲出边界和看涨行权价之间，获得本金和敲出票息
                                          如果在敲入边界和敲出边界之间，获得本金和红利票息"""
        self.v_not_in[:, -1] = np.where(s_vec <= self.next_barrier_in,
                                        np.where(s_vec <= prod.strike_lower, prod.strike_lower, s_vec) -
                                                 prod.strike_upper + prod.s0 * prod.margin_lvl,
                                        np.where(s_vec > prod.strike_call,
                                                 (s_vec - prod.strike_call) * prod.parti_out + (
                                                        prod.margin_lvl + self.next_coupon_out * coupon_t) * prod.s0,
                                                 np.where(s_vec >= self.next_barrier_out,
                                                          (prod.margin_lvl + self.next_coupon_out * coupon_t) * prod.s0,
                                                          (prod.margin_lvl + prod.coupon_div * coupon_t) * prod.s0)))
