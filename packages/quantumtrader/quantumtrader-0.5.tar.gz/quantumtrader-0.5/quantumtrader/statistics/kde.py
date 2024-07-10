from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import rcParams

rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def kde_plot(xr, kdy, density_threshold, high_density_index, max_density_index):
    plt.figure(figsize=(20, 15))
    plt.plot(xr, kdy, label='KDE', linestyle='--')
    threshold = np.percentile(kdy, density_threshold)
    plt.axhline(y=threshold,
                color='r',
                linestyle='--',
                label=f'{density_threshold}%阈值')
    plt.plot(xr[high_density_index],
             kdy[high_density_index],
             label='高密度区域',
             color="green")
    plt.axvline(x=xr[max_density_index],
                linestyle='-.',
                color='green',
                label='最高点',
                linewidth=0.7)
    plt.xlabel('收盘价')  # 使用 xlabel 而不是 set_xlabel
    plt.ylabel('概率密度')  # 使用 ylabel 而不是 set_ylabel
    plt.legend(loc='upper left')

    for start_idx, end_idx in zip(high_density_index[:-1],
                                  high_density_index[1:]):
        plt.axvspan(xr[start_idx], xr[end_idx], color='green', alpha=0.05)

    # 设置X轴为整数刻度
    ax = plt.gca()  # 获取当前坐标轴对象
    # 显示所有刻度
    # ax.set_xticks(np.arange(min(xr), max(xr)+1, 1))  # 设置X轴刻度为整数
    # 每隔5个刻度显示一个
    # ax.set_xticks(np.arange(min(xr), max(xr)+1, 5))
    # 转换X轴数据为对数形式
    # ax.set_xscale('log')
    # 可能需要重新设置刻度，以适应对数刻度
    # ax.set_xticks(10**np.arange(np.log10(min(xr)), np.log10(max(xr))+2))
    # 格式化刻度标签
    ax.set_xticklabels([int(x) if x.is_integer() else "" for x in ax.get_xticks()])
    plt.show()


def kde(close,
        volume,
        kde_factor: float = 0.05,
        density_threshold: int = 95,
        show_plot: bool = False):
    """kde指标，是一种核密度估计，通过高斯核进行密度集中区域评估，并加上交易量权重，可以发现交易集中的价格区间，可作为压力、阻力区间的参考

    Args:
        close ([type]): 收盘价
        volume ([type]): 交易量
        kde_factor (float, optional): 带宽，控制平滑程度. Defaults to 0.05.
        density_threshold (int, optional): 筛选阈值，可筛选第N个百分位作为参考. Defaults to 95.

    Returns:
        high_density_index: 高密度index
        high_density_prices : 高密度区域的价格
        max_density_index : 高密度区最高密度价格的index
        kdy : 对应收盘价的概率值（kdy）


        
        
        带宽，控制平滑程度. Defaults to 0.05.
        density_threshold : 筛选阈值，可筛选第N个百分位作为参考. Defaults to 95.

    """

    # 创建 KDE 对象，使用收盘价和成交量作为权重
    kde = stats.gaussian_kde(close, weights=volume, bw_method=kde_factor)
    # 定义评估点的范围，这里使用收盘价的最小值和最大值
    xr = np.linspace(close.min(), close.max(), len(close))
    # 计算收盘价点的概率密度
    kdy = kde(xr)
    threshold = np.percentile(kdy, density_threshold)  #返回数组的第N个百分位
    high_density_index = np.where(kdy > threshold)[0]  # 获取高密度index
    high_density_prices = xr[high_density_index]  #
    max_density_index = high_density_index[np.argmax(kdy[high_density_index])]

    if show_plot == True:
        kde_plot(xr, kdy, density_threshold, high_density_index,
                 max_density_index)

    return high_density_index, high_density_prices, max_density_index, kdy,
