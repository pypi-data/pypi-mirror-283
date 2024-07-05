#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C) 2024 Galaxy Technologies
Licensed under the Apache License, Version 2.0
"""
from abc import ABCMeta, abstractmethod
from contextlib import suppress
import datetime
import numpy as np
from ..time import global_evaluation_date
from ..pricing_engine_base.engine_base import PricingEngineBase


class OptionBase(metaclass=ABCMeta):
    """期权产品基类"""

    def __init__(self):
        """初始化
        engine: PricingEngine，定价引擎
        trade_calendar: TradeCalendar，交易日历
        end_date: datetime.date，到期日
        """
        self.engine = None
        self.trade_calendar = None
        self.end_date = None

    @abstractmethod
    def set_pricing_engine(self, engine):
        """设置定价引擎，指定当前的定价函数_pricing_func.
        根据产品类型，可能存在闭式解、蒙特卡洛模拟、PDE有限差分、积分法、树方法等定价方法。
        """

    @abstractmethod
    def __repr__(self):
        """返回期权的描述"""

    @abstractmethod
    def price(self, *args, **kwargs):
        """执行定价
        对于标的期初价格为s0的期权，以香草期权为例，返回的是BSM公式的定价结果，即max(0, St - K)期望的现值
        如果想要得到单位估值，需要再除以s0"""
        self.validate_parameters()

    def validate_parameters(self, t=None):
        """price方法中，先检查产品是否已经配置了定价引擎，估值日是否小于终止日
        Args:
            t: datetime.date，计算期权价格的日期，默认None，此时使用全局估值日"""
        if self.engine is None or not isinstance(self.engine, PricingEngineBase):
            raise AttributeError("尚未配置定价引擎，您可以在以下两种方法中选择:\n"
                                 "    1. 在产品类同时输入s,r,q,vol以创建默认定价引擎;\n"
                                 "    2. 自行创建定价引擎，再使用set_pricing_engine方法配置到产品中")
        calculate_date = global_evaluation_date() if t is None else t
        if calculate_date > self.end_date:
            raise ValueError(f"估值日必须小于等于到期日, 当前估值日为{calculate_date}, 到期日为{self.end_date}.\n"
                             f"默认估值日是今天。如需修改，请使用set_evaluation_date(datetime.date(2024, 5, 20))配置全局估值日。")

    def delta(self, spot=None, step=None, *args, **kwargs):
        """求价格spot处的delta值
        会先尝试调用定价引擎的delta方法，如果没有则使用通用的差分法计算
        Args:
            spot: float，价格的绝对值
            step: float，微扰步长，默认为价格spot的1%
        Returns: delta = ∂V/∂S
        """
        try:
            return self.engine.delta(prod=self, spot=spot, step=step, *args, **kwargs)
        except:
            self.validate_parameters()
            spot = self.engine.process.spot() if spot is None else spot
            step = spot * 0.01 if step is None else step
            up_price = self.price(spot=spot + step)
            down_price = self.price(spot=spot - step)
            delta = (up_price - down_price) / (2 * step)
            return delta

    def gamma(self, spot=None, step=None, *args, **kwargs):
        """求价格spot处的gamma值
        会先尝试调用定价引擎的gamma方法，如果没有则使用通用的差分法计算
        Args:
            spot: float，价格的绝对值
            step: float，微扰步长，默认为价格spot的1%
        Returns: gamma = ∂2V/∂S2
        """
        try:
            return self.engine.gamma(prod=self, spot=spot, step=step, *args, **kwargs)
        except:
            self.validate_parameters()
            spot = self.engine.process.spot() if spot is None else spot
            step = spot * 0.01 if step is None else step
            up_price = self.price(spot=spot + step)
            down_price = self.price(spot=spot - step)
            mid_price = self.price(spot=spot)
            gamma = (up_price - 2 * mid_price + down_price) / (step ** 2)
            return gamma

    def vega(self, spot=None, step=0.01, *args, **kwargs):
        """计算波动率上升1%的vega todo:目前只支持常数波动率
        会先尝试调用定价引擎的vega方法，如果没有则使用通用的差分法计算
        Args:
            t: int，期权价值矩阵的列(时间)的索引
            spot: float，价格的绝对值
            step: float，微扰步长，默认为1%
        Returns: vega = ∂V/∂σ
        """
        try:
            return self.engine.vega(prod=self, spot=spot, step=step, *args, **kwargs)
        except:
            self.validate_parameters()
            spot = self.engine.process.spot() if spot is None else spot
            last_vol = self.engine.process.vol.volval
            last_price = self.price(spot=spot)
            self.engine.process.vol.volval = last_vol + step
            new_price = self.price(spot=spot)
            self.engine.process.vol.volval = last_vol
            vega = (new_price - last_price)
            return vega

    def theta(self, spot=None, step=1, *args, **kwargs):
        """计算一天的theta值
        会先尝试调用定价引擎的theta方法，如果没有则使用通用的差分法计算
        Args:
            t: int，期权价值矩阵的列(时间)的索引
            spot: float，价格的绝对值
            step: int，时间步长，默认为1天
        Returns: theta = ∂V/∂t
        """
        try:
            return self.engine.theta(prod=self, spot=spot, step=step, *args, **kwargs)
        except:
            try:
                spot = self.engine.process.spot() if spot is None else spot
                step = datetime.timedelta(days=step)
                origin_price = self.price(spot=spot)
                next_date = self.trade_calendar.advance(global_evaluation_date(), step)
                new_price = self.price(t=next_date, spot=spot)
                theta = (new_price - origin_price)
                return theta
            except:  # 可能遇到到期日估值，无法计算theta
                calculate_date = global_evaluation_date()
                if calculate_date > self.trade_calendar.advance(self.end_date, datetime.timedelta(days=1)):
                    raise ValueError(f"估值日必须小于等于到期日, 当前估值日为{calculate_date}, 到期日为{self.end_date}.")
                return np.nan  # 到期日估值，无法计算theta,返回nan

    def rho(self, spot=None, step=0.01, *args, **kwargs):
        """计算无风险利率上升1%的rho todo:目前只支持常数无风险利率
        会先尝试调用定价引擎的rho方法，如果没有则使用通用的差分法计算
        Args:
            t: int，期权价值矩阵的列(时间)的索引
            spot: float，价格的绝对值
            step: float，微扰步长，默认为1%
        Returns: rho = ∂V/∂r
        """
        try:
            return self.engine.rho(prod=self, spot=spot, step=step, *args, **kwargs)
        except:
            self.validate_parameters()
            spot = self.engine.process.spot() if spot is None else spot
            last_r = self.engine.process.interest.data
            last_price = self.price(spot=spot)
            self.engine.process.interest.data = last_r + step
            new_price = self.price(spot=spot)
            self.engine.process.interest.data = last_r
            rho = (new_price - last_price)
            return rho

    def pv_and_greeks(self, spot=None, *args, **kwargs):
        """当一次性计算pv和5个greeks时，可以调用此函数，减少计算量
        会先尝试调用定价引擎的pv_and_greeks方法，如果没有则使用通用的差分法计算
        Args:
            t: int，期权价值矩阵的列(时间)的索引
            spot: float，价格的绝对值
        Returns:
            Dict[str:float]: {'pv': pv, 'delta': delta, 'gamma': gamma, 'theta': theta, 'vega': vega, 'rho': rho}
        """
        if hasattr(self.engine, "pv_and_greeks"):
            with suppress(AttributeError, ValueError):
                self.price()
                return self.engine.pv_and_greeks(prod=self, spot=spot, *args, **kwargs)
        self.validate_parameters()
        spot = self.engine.process.spot() if spot is None else spot
        pv = np.float64(self.price(spot=spot))
        s_step = spot * 0.01
        up_price = self.price(spot=spot + s_step)
        down_price = self.price(spot=spot - s_step)
        delta = (up_price - down_price) / (2 * s_step)
        gamma = (up_price - 2 * pv + down_price) / (s_step ** 2)

        last_vol = self.engine.process.vol.volval
        self.engine.process.vol.volval = last_vol + 0.01
        new_price = self.price(spot=spot)
        self.engine.process.vol.volval = last_vol
        vega = (new_price - pv)

        last_r = self.engine.process.interest.data
        self.engine.process.interest.data = last_r + 0.01
        new_price = self.price(spot=spot)
        self.engine.process.interest.data = last_r
        rho = (new_price - pv)

        try:  # 可能遇到到期日估值，无法计算theta
            t_step = datetime.timedelta(days=1)
            next_date = self.trade_calendar.advance(global_evaluation_date(), t_step)
            new_price = self.price(t=next_date, spot=spot)
            theta = (new_price - pv)
        except:
            theta = np.nan
        return {'pv': pv, 'delta': delta, 'gamma': gamma, 'vega': vega, 'theta': theta, 'rho': rho}
