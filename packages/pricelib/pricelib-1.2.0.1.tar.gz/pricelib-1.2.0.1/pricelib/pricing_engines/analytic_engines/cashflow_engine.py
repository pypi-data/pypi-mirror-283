#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C) 2024 Galaxy Technologies
Licensed under the Apache License, Version 2.0
"""
from pricelib.common.utilities.enums import CallPut, InOut, UpDown, ExerciseType, PaymentType
from pricelib.common.processes import StochProcessBase
from pricelib.common.pricing_engine_base import AnalyticEngine


class CashFlowEngine(AnalyticEngine):
    """现金流闭式解定价引擎
    主要用于计算票息收益等现金流的现值"""
    updown = UpDown.Down
    inout = InOut.In
    callput = CallPut.Call
    payment_type = PaymentType.Expire
    exercise_type = ExerciseType.American

    def __init__(self, stoch_process: StochProcessBase = None, *, s=None, r=None, q=0, vol=0):
        """
        初始化现金流闭式解定价引擎
        Args:
            stoch_process: StochProcessBase随机过程对象
        在未设置stoch_process时，(stoch_process=None)，会默认创建BSMprocess，需要输入以下变量进行初始化
            s: float，标的价格
            r: float，无风险利率
            q: float，分红/融券率
            vol: float，波动率
        """
        super().__init__(stoch_process=stoch_process, s=s, r=r, q=q, vol=vol)
        self.payment_date = None
        self.cashflow = None

    # pylint: disable=arguments-differ
    def calc_present_value(self, prod):
        """
        计算现金流现值
        Args:
            prod: Product产品对象
        Returns:
            pv: 现金流现值
        """
        pv = prod.cashflow * self.process.interest.disc_factor(t2=prod.payment_date)
        return pv
