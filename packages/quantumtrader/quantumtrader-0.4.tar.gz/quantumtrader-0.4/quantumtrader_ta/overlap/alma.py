import pandas as pd
import numpy as np


def alma(src: pd.Series,
         window_size: int = 9,
         offset: float = 0.85,
         sigma: float = 6.0) -> pd.Series:
    """Arnaud Legoux 移动平均线（ALMA）

        使用高斯分布来加权价格数据，以解决传统移动平均线如简单移动平均线（SMA）或指数移动平均线（EMA）所面临的滞后和平滑问

    Args:
        src (pd.Series):  数据源（e.g. data["close"]）
        window_size (int, optional):  窗口数量（ K线数量）. Defaults to 9.
        offset (float, optional):偏移量（向右或向左调整平均值的因子），控制平滑度(更接近1)和响应性(更接近0)之间的权衡. Defaults to 0.85.
        sigma (float, optional): 均线平滑度。Sigma越大，ALMA越平滑. Defaults to 6.0.

    Raises:
        ValueError: 源数据长度必须至少与窗口数（ K线数量）大小一样长

    Returns:
        pd.Series: alma
    """
    if len(src) < window_size:
        raise ValueError("源数据长度必须至少与窗口大小一样长")

    # 计算便宜了m和标准差s，调整 s 以匹配高斯函数中的指数项
    m = np.floor(offset * (window_size - 1)).astype(int)
    s = window_size / (2 * sigma**2)

    # 计算权重及归一化权重
    weights = np.exp(-0.5 * ((np.arange(window_size) - m)**2) / s)
    weights /= weights.sum()  # Normalize the weights

    # 使用卷积将权重应用于序列（这对于大型数组是高效的）
    result = np.convolve(src, weights, mode='valid')

    # 卷积操作会使结果缩短 'window_size - 1' 个元素
    # 因此，我们需要在结果前面添加 NaN 值以匹配原始序列的长度
    result = np.concatenate((np.full(window_size - 1, np.nan), result))

    return result.astype(np.float32)