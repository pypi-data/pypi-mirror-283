import pandas as pd
import numpy as np
import talib as ta

def hma(src: pd.Series, length: int = 9) -> pd.Series:
    """赫尔移动平均线-hma(Hull Moving Average)

    Args:
        src (pd.Series): 数据源（e.g. data["close"]）
        length (int, optional): 周期长度. Defaults to 9.

    Returns:
        pd.Series: hma
    """
    wma1 = 2 * ta.WMA(src, int(length / 2))
    wma2 = ta.WMA(src, length)
    diff = wma1 - wma2
    sqrtLength = round(np.sqrt(length))
    return ta.WMA(diff, sqrtLength)