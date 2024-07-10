import pandas as pd

import talib as ta


def dema(src: pd.Series, length: int = 15) -> pd.Series:
    """双重指数移动平均线-DEMA（Double Exponential Moving Average）

        DEMA旨在减少传统移动平均线产生的滞后性，并减少可能扭曲价格图表走势的“噪音”数量
        
        通过结合单一EMA和双层EMA来改善传统平均线的时间落后问题，从而更早地显示出价格反转的可能性

    Args:
        src (pd.Series): 数据源（e.g. data["close"]）
        length (int, optional): 周期长度. Defaults to 15.

    Returns:
        pd.Series: dema
    """
    e = ta.EMA(src, length)
    d = ta.EMA(e, length)
    return (2 * e - d).astype("float32")