import ccxt
import numpy as np
import pandas as pd


def get_exchange_info(symbol: str = 'BTC/USDT') -> dict:
    """获取市场信息

    Args:
        symbol (str, optional):交易对. Defaults to 'BTC/USDT'.

    Returns:
        dict:市场info
    """
    exchange = ccxt.binance()
    exchange.load_markets()
    market_info = exchange.market(symbol)
    return market_info


def get_key_in_dict(d: dict, target_key: str = None) -> list:
    """
    递归搜索字典，找到目标键的值。（如果有多个相同key，则输出多个value）
    :param dict: 字典，可能包含嵌套字典或列表。
    :param target_key: 要搜索的目标键。
    :return: 目标键对应的值的列表。
    """

    result = []
    if isinstance(d, dict):
        for key, value in d.items():
            if key == target_key:
                result.append(value)
            elif isinstance(value, (dict, list)):
                result.extend(get_key_in_dict(value, target_key))
    elif isinstance(d, list):
        for item in d:
            result.extend(get_key_in_dict(item, target_key))
    return result

def mintick_to(src:pd.Series=None, tick_size:float=None)->pd.Series:
    """转换tick

    Args:
        src ([type]): Series
        tick_size ([type]): 最小tick

    Returns:
        [type]: [description]
    """
    return np.round(src / tick_size) * tick_size

