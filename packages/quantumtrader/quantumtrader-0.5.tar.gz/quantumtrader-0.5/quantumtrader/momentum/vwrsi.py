# Momentum Indicators  动量指标
import pandas as pd
import numpy as np
from quantumtrader_ta.overlap import vwrma


def vwrsi(c: pd.Series, v: pd.Series, length: int = 14) -> pd.Series:
    """成交量加权相对强度指数-VWRSI（Volume Weighted Relative Strength Index）

    Args:
        c (pd.Series): 收盘价
        v (pd.Series): 成交量
        length (int, optional): 周期长度. Defaults to 14.

    Returns:
        pd.Series: vwrsi
    """
    change_c = c.diff()
    up = vwrma(
        np.maximum(change_c, 0),
        v,
        length,
    )
    down = vwrma(np.minimum(change_c, 0) * -1, v, length)  # 注意这里乘以-1来转换负值为正值
    # 计算rsi
    # 替换NaN值（如果rma返回NaN），因为除以零会导致NaN
    up[np.isinf(up)] = np.nan  # 替换无穷大值（如果rma可能返回它们）
    down[np.isinf(down)] = np.nan  # 替换无穷大值（如果rma可能返回它们）
    rsi = 100 - (100 / (1 + np.where(up == 0, 1, up / down)))
    rsi[np.isnan(rsi)] = 50  # 替换NaN值为50

    return rsi