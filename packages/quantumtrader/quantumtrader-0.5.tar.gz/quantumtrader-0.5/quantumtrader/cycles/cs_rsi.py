import numpy as np
import pandas as pd
import talib as ta
from quantumtrader_ta.overlap import hma

def cs_rsi(rsi: pd.Series=None, length: int = 14) -> pd.Series:
    """横盘or盘整强度-CS*（Consolidation Strength）,结合RSI指标使用

    判断行情状态找到横盘信号及趋势信号


    Args:
        src (pd.Series): 数据源（e.g. data["RSI"]）
        length (int, optional): 周期长度. Defaults to 14.

    Raises:
        ValueError: 周期长度必须大于0

    Returns:
        pd.Series: cs
    """
    if rsi is None:
        return None
    
    if len(rsi) < length:
        raise ValueError("src的长度必须大于或等于Length")

    # 方向判断（dir）
    dir_values = np.where(rsi > 50, 1, -1)
    df = pd.DataFrame({'dir': dir_values})
    # 条件判断（t）（即方向是否未改变）。如果相同，t设为1，否则设为0
    df['t'] = np.where(df['dir'] + df['dir'].shift(1).fillna(0) == 0, 1,
                       0)  # 处理NaN值
    # 在length周期内的总和来计算权重
    w = 1 / length
    # 简单移动平均（p）,
    p = ta.SMA(df["t"] * w, length).round(2)

    # 中间变量，设置为length的一半
    v = length / 2
    f = hma(p, round(v, 2)) * (v + (2 / 3) * v)
    f1 = hma(f, length * 2)
    result = np.maximum(f1, 0).astype(np.float32)
    return result


cs_rsi.__doc__ = \
"""横盘or盘整强度-CS*（Consolidation Strength）

    判断行情状态找到横盘信号及趋势信号

Args:
        src (pd.Series): 数据源（e.g. data["RSI"]）
        length (int, optional): 周期长度. Defaults to 14.

    Raises:
        ValueError: 周期长度必须大于0

    Returns:
        pd.Series: cs    
"""