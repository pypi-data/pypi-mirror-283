import pywt
import numpy as np
import pandas as pd
from pywt import wavedec
from pywt import waverec


def _mad(d, axis=None):
    """ 信号的平均绝对偏差 
    
    衡量数据集中数值相对于平均值的离散程度
    """
    return np.mean(np.absolute(d - np.mean(d, axis)), axis)


def wt(data, wavelet: str = None, level: int = None):
    """小波降噪处理

    Args:
        data (np.ndarray or pd.Series): 序列数据
        wavelet (str, optional): [description]. 小波离散函数，当为None时，默认使用db2函数，Defaults to None.
        level (int, optional): 最细分解层，提供了信号在最小尺度上的详细信息，最细分解层可以用于提取信号中的高频成分，这些成分通常包含了信号的细节特征，如边缘、纹理 . Defaults to None.
         如果为None时，默认使用2层分解层. 

    Returns:
        [type]: denoised 降噪后的结果
    """

    wavelet = 'db2' if wavelet is None else wavelet
    level = 2 if level is None else level  # 小波变换分解层次选择2，层数决定了小波变换的深度，层数越高，分解的越细致

    if isinstance(data, np.ndarray) and data.ndim == 1:
        data.reshape(-1)
    if isinstance(data, pd.Series):
        data = data.values

    # 小波去噪包括三个部分:分解、阈值化、重构
    # 1、分解

    level = int(level)
    wavelet = wavelet
    coeff = wavedec(data, wavelet, level=level)

    # 2、阈值化

    # 使用mad函数计算系数中第-level层（最细的分解层）的MAD，然后除以0.6745（这个值是标准正态分布的四分位距与标准差的比值，用于从MAD估计标准差）
    sigma = _mad(
        coeff[-level]) / 0.6745  # coeff[-level]近似系数数组，对应于最大尺度（第level层）的近似

    # 根据计算出的标准差sigma，乘以2的自然对数和训练数据长度的平方根，得到阈值。用于小波变换的软阈值处理
    threshold = sigma * np.sqrt(2 * np.log(len(data)))

    # 对每个系数i应用软阈值处理，使用计算出的threshold作为阈值,并更新coeff数组中除了最粗略层之外的所有系数
    coeff[1:] = (pywt.threshold(i, value=threshold, mode="soft")
                 for i in coeff[1:])  # 最粗略层（coeff[0]）通常不进行阈值处理，因为它包含了信号的主要信息

    # 3、重构
    denoised = waverec(coeff, wavelet)

    if len(data)!=len(denoised):
        denoised = denoised[:-1]

    return denoised


wt.__doc__=\
"""
小波变换（Wavelet Transform）是一种数学工具，用于分析信号或数据在不同尺度上的变化。在小波变换中，"小波"是一个函数，用于在不同的尺度和位置上与信号相乘以提取信息。不同的小波函数具有不同的特性，适用于不同类型的信号分析。

db2和db8是小波变换中使用的Daubechies小波的两种不同类型，它们属于连续小波变换中的Daubechies Compactly Supported Wavelets（Daubechies小波）系列。这些小波以它们的发明者Ingrid Daubechies的名字命名，并且通过一个参数来区分，该参数定义了小波支持的长度和消失矩的数量。以下是db2和db8之间的一些主要区别：

消失矩（Vanishing Moments）：

db2具有2个消失矩，这意味着它可以捕捉到信号中的2阶多项式成分。
db8具有8个消失矩，这意味着它可以捕捉到信号中的8阶多项式成分。
支持长度（Support Length）：

db2的支持长度较短，这意味着它在时域中的宽度较小，可以在较小的时间窗口内提供更精细的频率分辨。
db8的支持长度较长，时域中的宽度较大，可以提供更平滑的频率分辨。
频率分辨能力：

db2由于其较短的支持长度，通常在频率分辨上不如db8精细。
db8由于其较长的支持长度和更多的消失矩，可以提供更好的频率分辨能力。
适用性：

db2可能更适合于需要快速局部化和对信号的局部特征敏感的应用。
db8可能更适合于需要更平滑频率响应和对信号的全局特性敏感的应用。
计算复杂性：

由于db8具有更多的消失矩和更长的支持长度，其计算复杂性可能略高于db2。
在选择使用db2还是db8时，需要根据具体的应用场景和信号特性来决定。例如，如果信号中包含高频噪声或需要更精细的频率分辨，可能会选择使用db8。如果信号分析更侧重于局部特征，或者需要快速响应，则可能选择db2。


"""
