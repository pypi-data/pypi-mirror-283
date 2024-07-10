import pandas as pd

import talib as ta

def tema(src: pd.Series, length: int = 15) -> pd.Series:
    """三重指数移动平均线-TEMA（Triple Exponential Moving Average）

        通过平滑价格数据并识别趋势，三次平滑价格数据减少价格波动的影响

    Args:
        src (pd.Series):数据源（e.g. data["close"]）
        length (int, optional): 周期长度. Defaults to 15.

    Returns:
        pd.Series: tema
    """
    e = ta.EMA(src, length)
    ema_ema = ta.EMA(e, length)
    ema_ema_ema = ta.EMA(ema_ema, length)
    return (3 * (e - ema_ema) + ema_ema_ema).astype("float32")
