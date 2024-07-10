import pandas as pd
import numpy as np
from quantumtrader_ta.overlap import rma
def vwrma(src: pd.Series, volume: pd.Series, length: int = 14) -> pd.Series:
    """成交量加权移动均线-VWMA(Volume Weighted Moving Average)

    Args:
        src (pd.Series): 加权数据系列（e.g. 收盘价差值-data["close"].diff()）
        volume (pd.Series): 成交量
        length (int, optional): 周期长度. Defaults to 14.

    Returns:
        pd.Series: vwrma
    """
    result = rma(src * volume, length) / rma(volume, length)
    return result.astype(np.float32)