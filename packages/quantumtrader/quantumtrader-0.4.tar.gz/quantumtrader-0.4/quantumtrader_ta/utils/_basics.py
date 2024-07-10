# -*- coding: utf-8 -*-
from typing import Generator
from numbers import Integral
import numpy as np


__all__ = ['ifnone',"is_listy","convert_date_format"]

def ifnone(a, b):
    "如果a是None，则返回b，否则返回a"
    return b if a is None else a

def is_listy(x):
    "检查x是否是tuple（元组）、list（列表）或slice（切片）类型，或者是生成器迭代器"
    return isinstance(x, (tuple,list,slice,Generator))   


def smallest_dtype(num, use_unsigned=False):
    """找到能安全地保存数值的最小的dtype

    Args:
        num ([type]): 数字
        use_unsigned (bool, optional):是否使用无符号. Defaults to False.

    Returns:
        [type]: [description]
    """

    if use_unsigned:
        int_dtypes = ['uint8', 'uint16', 'uint32', 'uint64']
        float_dtypes = ['float16', 'float32']
        float_bounds = [2**11, 2**24] # 2048, 16777216
    else:
        int_dtypes = ['int8', 'int16', 'int32', 'int64']
        float_dtypes = ['float16', 'float32', 'float64']
        float_bounds = [2**11, 2**24, 2**53] # 2048, 16777216, 9007199254740992
    if isinstance(num, Integral):
        for dtype in int_dtypes:
            if np.iinfo(dtype).min <= num <= np.iinfo(dtype).max:
                return np.dtype(dtype)
        raise ValueError("没有找到dtype")
    elif isinstance(num, float):
        for dtype, bound in zip(float_dtypes, float_bounds):
            num = round(num)
            if -bound <= num <= bound:
                return np.dtype(dtype)
        raise ValueError("没有找到dtype")
    else:
        raise ValueError("输入的不是一个数值") 
    

def convert_date_format(data):
    data['data_no_z_t'] = data['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    data['date_only'] = data['date'].dt.date
    data['time_only'] = data['date'].dt.time
    return data