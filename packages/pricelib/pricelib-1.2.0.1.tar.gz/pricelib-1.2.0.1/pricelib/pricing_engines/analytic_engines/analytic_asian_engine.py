#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C) 2024 Galaxy Technologies
Licensed under the Apache License, Version 2.0
"""

import math
from scipy.stats import norm
from pricelib.common.utilities.enums import AverageMethod, AsianAveSubstitution, CallPut
from pricelib.common.time import global_evaluation_date
from pricelib.common.pricing_engine_base import AnalyticEngine


class AnalyticAsianEngine(AnalyticEngine):
    """亚式期权闭式解定价引擎  # todo:若定价时已经处于均价观察期内，需要获得当前已经实现的均价，并对行权价进行调整
    Kemma Vorst 1990 支持几何平均价格替代标的资产价格的亚式期权. 仅支持期初估值. 连续观察，平均价观察期为整个期权有效期内
    Turnbull Wakeman 1991 近似估计 支持算术平均价格替代标的资产价格的亚式期权. 平均观察期的起点任意，终点为期权到期日
    todo: 利用固定行权价与浮动行权价亚式期权的对称性，定价平均行权价亚式"""

    # pylint: disable=invalid-name, too-many-locals
    def calc_present_value(self, prod, t=None, spot=None):
        """计算现值
        Args:
            prod: Product产品对象
            t: datetime.date，估值日; 如果是None，则使用全局估值日globalEvaluationDate
            spot: float，估值日标的价格，如果是None，则使用随机过程的当前价格
        Returns: float，现值
        """
        assert not prod.enhanced, "Error: 亚式期权解析解引擎不支持增强亚式期权"
        assert prod.substitute == AsianAveSubstitution.Underlying, "Error: 亚式期权解析解引擎只支持平均结算价，不支持平均执行价"
        calculate_date = global_evaluation_date() if t is None else t
        # T = (prod.end_date - calculate_date).days / prod.annual_days.value
        _maturity_business_days = prod.trade_calendar.business_days_between(calculate_date, prod.end_date)
        T = _maturity_business_days / prod.t_step_per_year
        obs_start = prod.trade_calendar.business_days_between(calculate_date, prod.obs_start)
        obs_end = prod.trade_calendar.business_days_between(calculate_date, prod.obs_end)
        if spot is None:
            spot = self.process.spot()
        r = self.process.interest(T)
        q = self.process.div(T)
        vol = self.process.vol(T, self.process.spot())
        b = r - q
        if prod.ave_method == AverageMethod.Geometric:
            # Kemna Vorst 1990 几何平均收盘价替代标的资产价格的亚式期权
            assert (obs_start <= 0 and obs_end == _maturity_business_days), \
                "Error: 几何平均亚式期权解析解的观察开始日必须是估值日，观察结束日必须是到期日"
            b_A = 0.5 * (b - vol ** 2 / 6)
            vol_A = vol / math.sqrt(3)

            d1 = (math.log(spot / prod.strike) + (b_A + 0.5 * vol_A ** 2) * T) / (vol_A * math.sqrt(T))
            d2 = d1 - vol_A * math.sqrt(T)

            price = prod.callput.value * (spot * math.exp((b_A - r) * T) * norm.cdf(prod.callput.value * d1)
                                          - prod.strike * math.exp(-r * T) * norm.cdf(prod.callput.value * d2))
            return price

        elif prod.ave_method == AverageMethod.Arithmetic:
            # Turnbull Wakeman 1991近似估计 算术平均收盘价替代标的资产价格的亚式期权
            assert obs_end == _maturity_business_days, "Error: 算术平均亚式期权解析解的观察结束日必须是到期日"

            t1 = max(obs_start, 0) / prod.t_step_per_year
            T2 = (obs_end - obs_start) / prod.t_step_per_year
            tau = T2 - T
            if b == 0:  # 此时公式可以简化
                M1 = 1
            else:
                M1 = (math.exp(b * T) - math.exp(b * t1)) / (b * T - b * t1)
            if tau > 0:  # 若此时在资产价格平均期内，tau = T2 - T > 0
                assert prod.s_average is not None, "Error: 已经处于资产价格平均期内时，必须输入已实现的资产价格平均值s_average"
                strike_hat = T2 / T * prod.strike - tau / T * prod.s_average
                if strike_hat < 0:  # 此时认购期权一定会行权，认沽期权必然不是实值期权，价格为0
                    if prod.callput == CallPut.Call:
                        # 到期时的标的资产平均价格的期望值
                        s_a = prod.s_average * (T2 - T) / T2 + spot * M1 * T / T2
                        return max(s_a - prod.strike, 0) * math.exp(-r * T)
                    else:
                        return 0
            else:
                strike_hat = prod.strike

            if b == 0:
                M2 = (2 * math.exp(vol ** 2 * T) - 2 * math.exp(vol ** 2 * t1) * (1 + vol ** 2 * (T - t1))) / (
                        vol ** 4 * (T - t1) ** 2)
            else:
                M2 = (2 * math.exp((2 * b + vol ** 2) * T)) / ((b + vol ** 2) * (2 * b + vol ** 2) * (T - t1) ** 2) + \
                     (2 * math.exp((2 * b + vol ** 2) * t1)) / (b * (T - t1) ** 2) * (
                             1 / (2 * b + vol ** 2) - (math.exp(b * (T - t1)) / (b + vol ** 2)))

            b_A = math.log(M1) / T
            vol_A = math.sqrt(math.log(M2) / T - 2 * b_A)

            d1 = (math.log(spot / strike_hat) + (b_A + 0.5 * vol_A ** 2) * T) / (vol_A * math.sqrt(T))
            d2 = d1 - vol_A * math.sqrt(T)

            price = prod.callput.value * (spot * math.exp((b_A - r) * T) * norm.cdf(prod.callput.value * d1)
                                          - strike_hat * math.exp(-r * T) * norm.cdf(prod.callput.value * d2))
            if tau > 0:
                price = price * T / T2
            return price

        else:
            raise ValueError("未知的平均方式，亚式平均方式为几何平均/算术平均")
