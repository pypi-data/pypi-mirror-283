import pandas as pd
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Union
from warnings import simplefilter
from pandas.core.base import PandasObject
# from multiprocessing import cpu_count, Pool
from quantumtrader_ta.utils import *
from time import perf_counter
from quantumtrader_ta import Category,version
from quantumtrader_ta.candles import *
from quantumtrader_ta.cycles import *
from quantumtrader_ta.performance import *
from quantumtrader_ta.momentum import *
from quantumtrader_ta.overlap import *
from quantumtrader_ta.statistics import *
from quantumtrader_ta.trend import *
from quantumtrader_ta.volatility import *
from quantumtrader_ta.volume import *
from quantumtrader_ta.qtai import *


df = pd.DataFrame()

# 基础类扩展Pandas DataFrame
class BasePandasObject(PandasObject):
    """简单的Pandas基类

    Args:
        df (pd.DataFrame): 扩展Pandas DataFrame
    """

    def __init__(self, df, **kwargs):
        # 确保DataFrame不为空并且有列
        if df.empty: return
        if len(df.columns) > 0:
            common_names = {
                "Date": "date",
                "Time": "time",
                "Timestamp": "timestamp",
                "Datetime": "datetime",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                # "Adj Close": "adj_close",
                "Volume": "volume",
                # "Dividends": "dividends",
                # "Stock Splits": "split",
            }
            # 删除全是NaN的行
            df.dropna(axis=0, inplace=True)
            
            # 可能需要移动到AnalysisIndicators.__call__()中，以便通过kwargs进行切换

            # 重命名列表名
            df.rename(columns=common_names, errors="ignore", inplace=True)

            # 将列名改为小写
            index_name = df.index.name
            if index_name is not None:
                df.index.rename(index_name.lower(), inplace=True)

            self._df = df
        else:
            raise AttributeError(f"错误： 没有列表名")

    def __call__(self, kind, *args, **kwargs):
        raise NotImplementedError()


# 通过装饰器给DataFrame添加拓展访问器
@pd.api.extensions.register_dataframe_accessor("qta")
class AnalysisIndicators(BasePandasObject):
    """
    这个指标库的扩展名为'qta'（QchainDym Technical Analysis）。换句话说，给定一个dataframe(列表名为小写)，可以通过.qta属性来访问
    AnalysisIndicators类的方法和属性

    默认情况下，'qta'使用小写列名：open、high、low、close和volume

    例子1：使用默认的列名：open, high, low, close, volume.
    >>> df.qta.hl2()
    >>> df.qta(kind="hl2")   

    例子2：使用DataFrame（客户导入的）的列名：Open, High, Low, Close, and Volume.
    >>> df.qta.hl2(high="High", low="Low")
    >>> df.qta(kind="hl2", high="High", low="Low")

    例子3：如果您不想使用DataFrame扩展，只需正常调用即可
    >>> sma10 = qta.sma(df["Close"]) # 默认周期length=10
    >>> sma50 = qta.sma(df["Close"], length=50)
    >>> ichimoku, span = qta.ichimoku(df["High"], df["Low"], df["Close"])
    
    Args:

        kind (str, optional): Default: None. 指标名称，在调用前将其转换为小写.
        
        timed (bool, optional): Default: False. 运行速度
        kwargs: 拓展的关键字.
            append (bool, optional): Default: False. 添加结果至DataFrame中，当设置为True时，执行添加
    
    Returns:
        大多数指标将返回一个Pandas Series。其他一些指标，如MACD、BBANDS、KC等，将返回一个Pandas DataFrame。
        
        另一方面，Ichimoku将返回两个DataFrame，一个是已知周期的Ichimoku DataFrame，另一个是Span值的未来Span DataFrame。
    
    """

    _adjusted = None
    _df = pd.DataFrame()

    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._df = pandas_obj


    @staticmethod
    def _validate(obj: Tuple[pd.DataFrame, pd.Series]):
        """验证数据源有效性，是否为pd.DataFrame或pd.Series"""
        if not isinstance(obj, pd.DataFrame) and not isinstance(
                obj, pd.Series):
            raise AttributeError("错误：数据源必须是Pandas Series或DataFrame")

    # 调用方法
    def __call__(self,
                 kind: str = None,
                 version: bool = False,
                 **kwargs):
        """AI is creating summary for __call__

        Args:
            kind (str, optional): 指标类型. Defaults to None.
            version (bool, optional): 版本号. Defaults to False.

        Returns:
            [type]: [description]
        """
        if version: print(f"QchainDym TA - 技术分析指标 - v{version}")
        try:
            if isinstance(kind, str):
                kind = kind.lower()
                fn = getattr(self, kind)

                if timed:
                    stime = perf_counter()

                # 执行指标
                result = fn(**kwargs)  # = getattr(self, kind)(**kwargs)
                self._last_run = get_time(
                    self.exchange,
                    to_string=True)  # Save when it completed it's run

                return result
            else:
                self.help()

        except BaseException:
            pass

    @property
    def adjusted(self) -> str:
        """属性: df.ta.adjusted"""
        return self._adjusted

    @adjusted.setter
    def adjusted(self, value: str) -> None:
        """属性: df.ta.adjusted = 'adj_close'"""
        if value is not None and isinstance(value, str):
            self._adjusted = value
        else:
            self._adjusted = None

    @property
    def categories(self) -> str:
        """返回类别"""
        return list(Category.keys())

    def _indicators_by_category(self, name: str) -> list:
        """根据分类名称返回指标."""
        return Category[name] if name in self.categories else None

    def _get_column(self, series):
        """获取列名"""
        df = self._df
        if df is None: return

        # 传递一个pd.Series来覆盖默认值
        if isinstance(series, pd.Series):
            return series
        # 如果没有序列也没有默认值，则应用默认值
        elif series is None:
            return df[self.adjusted] if self.adjusted is not None else None

        elif isinstance(series, str):
            # 返回df列
            if series in df.columns:
                return df[series]
            else:
                # 尝试匹配“series”，因为它可能拼写错误了
                matches = df.columns.str.match(series, case=False)
                match = [i for i, x in enumerate(matches) if x]
                cols = ", ".join(list(df.columns))
                NOT_FOUND = f"错误： {series not in df.columns}, 在 {cols} 中，并未找到 '{series}' 列名"
                return df.iloc[:, match[0]] if len(match) else print(NOT_FOUND)

    def _mp_worker(self, arguments: tuple):
        """多进程工作进程，用于处理不同的方法"""
        method, args, kwargs = arguments

        if method != "ichimoku":
            return getattr(self, method)(*args, **kwargs)
        else:
            return getattr(self, method)(*args, **kwargs)[0]

    def _add_prefix_suffix(self, result=None, **kwargs) -> None:
        """向结果列添加前缀和/或后缀"""
        if result is None:
            return
        else:
            prefix = suffix = ""
            # setdefault 方法:从 kwargs 字典中尝试获取 "delimiter" 键的值，如果该键不存在，则设置其默认值为 "_"，并返回该值
            delimiter = kwargs.setdefault("delimiter", "_")

            if "prefix" in kwargs:
                prefix = f"{kwargs['prefix']}{delimiter}"
            if "suffix" in kwargs:
                suffix = f"{delimiter}{kwargs['suffix']}"

            if isinstance(result, pd.Series):
                result.name = prefix + result.name + suffix
            else:
                result.columns = [
                    prefix + column + suffix for column in result.columns
                ]

    def _append(self, result=None, **kwargs) -> None:
        """将Pandas Series或DataFrame列追加到self._df"""
        if "append" in kwargs and kwargs["append"]:
            df = self._df
            if df is None or result is None: return
            else:
                simplefilter(action="ignore",
                             category=pd.errors.PerformanceWarning)
                # 检查kwargs["col_names"]是否为元组，如果不是元组需要转换为元组类型
                if "col_names" in kwargs and not isinstance(
                        kwargs["col_names"], tuple):
                    kwargs["col_names"] = (
                        kwargs["col_names"],
                    )  # Note: tuple(kwargs["col_names"]) doesn't work

                if isinstance(result, pd.DataFrame):
                    # 如果在kwargs中指定，则重命名列.
                    # 如果没有，则使用默认名称
                    if "col_names" in kwargs and isinstance(
                            kwargs["col_names"], tuple):
                        if len(kwargs["col_names"]) >= len(result.columns):
                            for col, ind_name in zip(result.columns,
                                                     kwargs["col_names"]):
                                df[ind_name] = result.loc[:, col]
                        else:
                            print(
                                f"指定的列名称数量不足: 需要 {len(result.columns)}个，但只有 {len(kwargs['col_names'])}"
                            )
                            return
                    else:
                        for i, column in enumerate(result.columns):
                            df[column] = result.iloc[:, i]
                else:
                    ind_name = (kwargs["col_names"][0] if "col_names" in kwargs
                                and isinstance(kwargs["col_names"], tuple) else
                                result.name)
                    df[ind_name] = result

    def _post_process(self, result: Union[pd.Series, pd.DataFrame],
                      **kwargs) -> Tuple[pd.Series, pd.DataFrame]:
        """对DataFrame进行任何额外的修改
        * 应用前缀和/或后缀
        * 将结果追加到主DataFrame

        Args:
            result (Union[pd.Series, pd.DataFrame]): 需要添加到dataframe的数据序列
            
            kwargs:
                verbose:控制函数是否输出详细的调试或错误信息,设置为True（或者如果没有在kwargs中指定而使用了默认值 False），打印信息
                
                col_numbers: 只将特定的列追加到DataFrame中，元组类型，例如：'col_numbers':(0,1,3)

                prefix：前缀名称，例如：'prefix':'15m'

                suffix：后缀名称，例如：'suffix':'5m'

                append：是否将结果追加到DataFrame，当True时，添加，默认为不添加

                col_names：追加到DataFrame的列名，元组类型，例如：'col_numbers':("ma3","SMA",...)


        Returns:
            Tuple[pd.Series, pd.DataFrame]: 
        """

        verbose = kwargs.pop("verbose", False)
        if not isinstance(result, (pd.Series, pd.DataFrame)):
            if verbose:
                print(f"[X] 错误： 结果不是Series或DataFrame")
            return self._df
        else:
            result = (result.iloc[:, [int(n) for n in kwargs["col_numbers"]]]
                      if isinstance(result, pd.DataFrame)
                      and "col_numbers" in kwargs
                      and kwargs["col_numbers"] is not None else result)
            # 添加前缀/后缀并追加到DataFrame中
            self._add_prefix_suffix(result=result, **kwargs)
            self._append(result=result, **kwargs)
        return result

    

    # k线指标
    def cdl_pattern(self, name="all", offset=None, **kwargs):
        open_ = self._get_column(kwargs.pop("open", "open"))
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = cdl_pattern(open_=open_, high=high, low=low, close=close, name=name, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def cdl_z(self, full=None, offset=None, **kwargs):
        open_ = self._get_column(kwargs.pop("open", "open"))
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = cdl_z(open_=open_, high=high, low=low, close=close, full=full, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def ha(self, offset=None, **kwargs):
        open_ = self._get_column(kwargs.pop("open", "open"))
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = ha(open_=open_, high=high, low=low, close=close, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    # 周期指标
    def ebsw(self, close=None, length=None, bars=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = ebsw(close=close,
                      length=length,
                      bars=bars,
                      offset=offset,
                      **kwargs)
        return self._post_process(result, **kwargs)
    def cs(self, close=None, length=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = cs(src=close,
                      length=length,
                      **kwargs)
        return self._post_process(result, **kwargs)
    

    # 动量指标
    def ao(self, fast=None, slow=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        result = ao(high=high,
                    low=low,
                    fast=fast,
                    slow=slow,
                    offset=offset,
                    **kwargs)
        return self._post_process(result, **kwargs)

    def apo(self, fast=None, slow=None, mamode=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = apo(close=close,
                     fast=fast,
                     slow=slow,
                     mamode=mamode,
                     offset=offset,
                     **kwargs)
        return self._post_process(result, **kwargs)

    def bias(self, length=None, mamode=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = bias(close=close,
                      length=length,
                      mamode=mamode,
                      offset=offset,
                      **kwargs)
        return self._post_process(result, **kwargs)

    def bop(self, percentage=False, offset=None, **kwargs):
        open_ = self._get_column(kwargs.pop("open", "open"))
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = bop(open_=open_,
                     high=high,
                     low=low,
                     close=close,
                     percentage=percentage,
                     offset=offset,
                     **kwargs)
        return self._post_process(result, **kwargs)

    def brar(self,
             length=None,
             scalar=None,
             drift=None,
             offset=None,
             **kwargs):
        open_ = self._get_column(kwargs.pop("open", "open"))
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = brar(open_=open_,
                      high=high,
                      low=low,
                      close=close,
                      length=length,
                      scalar=scalar,
                      drift=drift,
                      offset=offset,
                      **kwargs)
        return self._post_process(result, **kwargs)

    def cci(self, length=None, c=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = cci(high=high,
                     low=low,
                     close=close,
                     length=length,
                     c=c,
                     offset=offset,
                     **kwargs)
        return self._post_process(result, **kwargs)

    def cfo(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = cfo(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def cg(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = cg(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def cmo(self, length=None, scalar=None, drift=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = cmo(close=close,
                     length=length,
                     scalar=scalar,
                     drift=drift,
                     offset=offset,
                     **kwargs)
        return self._post_process(result, **kwargs)

    def coppock(self,
                length=None,
                fast=None,
                slow=None,
                offset=None,
                **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = coppock(close=close,
                         length=length,
                         fast=fast,
                         slow=slow,
                         offset=offset,
                         **kwargs)
        return self._post_process(result, **kwargs)

    def cti(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = cti(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def dm(self, drift=None, offset=None, mamode=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        result = dm(high=high,
                    low=low,
                    drift=drift,
                    mamode=mamode,
                    offset=offset,
                    **kwargs)
        return self._post_process(result, **kwargs)

    def er(self, length=None, drift=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = er(close=close,
                    length=length,
                    drift=drift,
                    offset=offset,
                    **kwargs)
        return self._post_process(result, **kwargs)

    def eri(self, length=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = eri(high=high,
                     low=low,
                     close=close,
                     length=length,
                     offset=offset,
                     **kwargs)
        return self._post_process(result, **kwargs)

    def fisher(self, length=None, signal=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        result = fisher(high=high,
                        low=low,
                        length=length,
                        signal=signal,
                        offset=offset,
                        **kwargs)
        return self._post_process(result, **kwargs)

    def inertia(self,
                length=None,
                rvi_length=None,
                scalar=None,
                refined=None,
                thirds=None,
                mamode=None,
                drift=None,
                offset=None,
                **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        if refined is not None or thirds is not None:
            high = self._get_column(kwargs.pop("high", "high"))
            low = self._get_column(kwargs.pop("low", "low"))
            result = inertia(close=close,
                             high=high,
                             low=low,
                             length=length,
                             rvi_length=rvi_length,
                             scalar=scalar,
                             refined=refined,
                             thirds=thirds,
                             mamode=mamode,
                             drift=drift,
                             offset=offset,
                             **kwargs)
        else:
            result = inertia(close=close,
                             length=length,
                             rvi_length=rvi_length,
                             scalar=scalar,
                             refined=refined,
                             thirds=thirds,
                             mamode=mamode,
                             drift=drift,
                             offset=offset,
                             **kwargs)

        return self._post_process(result, **kwargs)

    def kdj(self, length=None, signal=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = kdj(high=high,
                     low=low,
                     close=close,
                     length=length,
                     signal=signal,
                     offset=offset,
                     **kwargs)
        return self._post_process(result, **kwargs)

    def kst(self,
            roc1=None,
            roc2=None,
            roc3=None,
            roc4=None,
            sma1=None,
            sma2=None,
            sma3=None,
            sma4=None,
            signal=None,
            offset=None,
            **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = kst(close=close,
                     roc1=roc1,
                     roc2=roc2,
                     roc3=roc3,
                     roc4=roc4,
                     sma1=sma1,
                     sma2=sma2,
                     sma3=sma3,
                     sma4=sma4,
                     signal=signal,
                     offset=offset,
                     **kwargs)
        return self._post_process(result, **kwargs)

    def macd(self, fast=None, slow=None, signal=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = macd(close=close,
                      fast=fast,
                      slow=slow,
                      signal=signal,
                      offset=offset,
                      **kwargs)
        return self._post_process(result, **kwargs)

    def mom(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = mom(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def pgo(self, length=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = pgo(high=high,
                     low=low,
                     close=close,
                     length=length,
                     offset=offset,
                     **kwargs)
        return self._post_process(result, **kwargs)

    def ppo(self,
            fast=None,
            slow=None,
            scalar=None,
            mamode=None,
            offset=None,
            **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = ppo(close=close,
                     fast=fast,
                     slow=slow,
                     scalar=scalar,
                     mamode=mamode,
                     offset=offset,
                     **kwargs)
        return self._post_process(result, **kwargs)

    def psl(self,
            open_=None,
            length=None,
            scalar=None,
            drift=None,
            offset=None,
            **kwargs):
        if open_ is not None:
            open_ = self._get_column(kwargs.pop("open", "open"))

        close = self._get_column(kwargs.pop("close", "close"))
        result = psl(close=close,
                     open_=open_,
                     length=length,
                     scalar=scalar,
                     drift=drift,
                     offset=offset,
                     **kwargs)
        return self._post_process(result, **kwargs)

    def pvo(self,
            fast=None,
            slow=None,
            signal=None,
            scalar=None,
            offset=None,
            **kwargs):
        volume = self._get_column(kwargs.pop("volume", "volume"))
        result = pvo(volume=volume,
                     fast=fast,
                     slow=slow,
                     signal=signal,
                     scalar=scalar,
                     offset=offset,
                     **kwargs)
        return self._post_process(result, **kwargs)

    def qqe(self,
            length=None,
            smooth=None,
            factor=None,
            mamode=None,
            offset=None,
            **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = qqe(close=close,
                     length=length,
                     smooth=smooth,
                     factor=factor,
                     mamode=mamode,
                     offset=offset,
                     **kwargs)
        return self._post_process(result, **kwargs)

    def roc(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = roc(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def rsi(self, length=None, scalar=None, drift=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = rsi(close=close,
                     length=length,
                     scalar=scalar,
                     drift=drift,
                     offset=offset,
                     **kwargs)
        return self._post_process(result, **kwargs)

    def rsx(self, length=None, drift=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = rsx(close=close,
                     length=length,
                     drift=drift,
                     offset=offset,
                     **kwargs)
        return self._post_process(result, **kwargs)

    def rvgi(self, length=None, swma_length=None, offset=None, **kwargs):
        open_ = self._get_column(kwargs.pop("open", "open"))
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = rvgi(open_=open_,
                      high=high,
                      low=low,
                      close=close,
                      length=length,
                      swma_length=swma_length,
                      offset=offset,
                      **kwargs)
        return self._post_process(result, **kwargs)

    def slope(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = slope(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def smi(self,
            fast=None,
            slow=None,
            signal=None,
            scalar=None,
            offset=None,
            **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = smi(close=close,
                     fast=fast,
                     slow=slow,
                     signal=signal,
                     scalar=scalar,
                     offset=offset,
                     **kwargs)
        return self._post_process(result, **kwargs)

    def squeeze(self,
                bb_length=None,
                bb_std=None,
                kc_length=None,
                kc_scalar=None,
                mom_length=None,
                mom_smooth=None,
                use_tr=None,
                mamode=None,
                offset=None,
                **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = squeeze(high=high,
                         low=low,
                         close=close,
                         bb_length=bb_length,
                         bb_std=bb_std,
                         kc_length=kc_length,
                         kc_scalar=kc_scalar,
                         mom_length=mom_length,
                         mom_smooth=mom_smooth,
                         use_tr=use_tr,
                         mamode=mamode,
                         offset=offset,
                         **kwargs)
        return self._post_process(result, **kwargs)

    def squeeze_pro(self,
                    bb_length=None,
                    bb_std=None,
                    kc_length=None,
                    kc_scalar_wide=None,
                    kc_scalar_normal=None,
                    kc_scalar_narrow=None,
                    mom_length=None,
                    mom_smooth=None,
                    use_tr=None,
                    mamode=None,
                    offset=None,
                    **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = squeeze_pro(high=high,
                             low=low,
                             close=close,
                             bb_length=bb_length,
                             bb_std=bb_std,
                             kc_length=kc_length,
                             kc_scalar_wide=kc_scalar_wide,
                             kc_scalar_normal=kc_scalar_normal,
                             kc_scalar_narrow=kc_scalar_narrow,
                             mom_length=mom_length,
                             mom_smooth=mom_smooth,
                             use_tr=use_tr,
                             mamode=mamode,
                             offset=offset,
                             **kwargs)
        return self._post_process(result, **kwargs)

    def stc(self,
            ma1=None,
            ma2=None,
            osc=None,
            tclength=None,
            fast=None,
            slow=None,
            factor=None,
            offset=None,
            **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = stc(close=close,
                     ma1=ma1,
                     ma2=ma2,
                     osc=osc,
                     tclength=tclength,
                     fast=fast,
                     slow=slow,
                     factor=factor,
                     offset=offset,
                     **kwargs)
        return self._post_process(result, **kwargs)

    def stoch(self,
              fast_k=None,
              slow_k=None,
              slow_d=None,
              mamode=None,
              offset=None,
              **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = stoch(high=high,
                       low=low,
                       close=close,
                       fast_k=fast_k,
                       slow_k=slow_k,
                       slow_d=slow_d,
                       mamode=mamode,
                       offset=offset,
                       **kwargs)
        return self._post_process(result, **kwargs)

    def stochrsi(self,
                 length=None,
                 rsi_length=None,
                 k=None,
                 d=None,
                 mamode=None,
                 offset=None,
                 **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = stochrsi(high=high,
                          low=low,
                          close=close,
                          length=length,
                          rsi_length=rsi_length,
                          k=k,
                          d=d,
                          mamode=mamode,
                          offset=offset,
                          **kwargs)
        return self._post_process(result, **kwargs)

    def td_seq(self, asint=None, offset=None, show_all=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = td_seq(close=close,
                        asint=asint,
                        offset=offset,
                        show_all=show_all,
                        **kwargs)
        return self._post_process(result, **kwargs)

    def trix(self,
             length=None,
             signal=None,
             scalar=None,
             drift=None,
             offset=None,
             **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = trix(close=close,
                      length=length,
                      signal=signal,
                      scalar=scalar,
                      drift=drift,
                      offset=offset,
                      **kwargs)
        return self._post_process(result, **kwargs)

    def tsi(self,
            fast=None,
            slow=None,
            drift=None,
            mamode=None,
            offset=None,
            **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = tsi(close=close,
                     fast=fast,
                     slow=slow,
                     drift=drift,
                     mamode=mamode,
                     offset=offset,
                     **kwargs)
        return self._post_process(result, **kwargs)

    def uo(self,
           fast=None,
           medium=None,
           slow=None,
           fast_w=None,
           medium_w=None,
           slow_w=None,
           drift=None,
           offset=None,
           **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = uo(high=high,
                    low=low,
                    close=close,
                    fast=fast,
                    medium=medium,
                    slow=slow,
                    fast_w=fast_w,
                    medium_w=medium_w,
                    slow_w=slow_w,
                    drift=drift,
                    offset=offset,
                    **kwargs)
        return self._post_process(result, **kwargs)

    def willr(self, length=None, percentage=True, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = willr(high=high,
                       low=low,
                       close=close,
                       length=length,
                       percentage=percentage,
                       offset=offset,
                       **kwargs)
        return self._post_process(result, **kwargs)

    # 重叠指标
    def alma(self, length=None, sigma=None, distribution_offset=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = alma(close=close, length=length, sigma=sigma, distribution_offset=distribution_offset, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def dema(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = dema(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def ema(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = ema(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def fwma(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = fwma(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def hilo(self, high_length=None, low_length=None, mamode=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = hilo(high=high, low=low, close=close, high_length=high_length, low_length=low_length, mamode=mamode, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def hl2(self, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        result = hl2(high=high, low=low, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def hlc3(self, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = hlc3(high=high, low=low, close=close, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def hma(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = hma(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def hwma(self, na=None, nb=None, nc=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = hwma(close=close, na=na, nb=nb, nc=nc, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def jma(self, length=None, phase=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = jma(close=close, length=length, phase=phase, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def kama(self, length=None, fast=None, slow=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = kama(close=close, length=length, fast=fast, slow=slow, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def ichimoku(self, tenkan=None, kijun=None, senkou=None, include_chikou=True, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result, span = ichimoku(high=high, low=low, close=close, tenkan=tenkan, kijun=kijun, senkou=senkou, include_chikou=include_chikou, offset=offset, **kwargs)
        self._add_prefix_suffix(result, **kwargs)
        self._add_prefix_suffix(span, **kwargs)
        self._append(result, **kwargs)
        # return self._post_process(result, **kwargs), span
        return result, span

    def linreg(self, length=None, offset=None, adjust=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = linreg(close=close, length=length, offset=offset, adjust=adjust, **kwargs)
        return self._post_process(result, **kwargs)

    def mcgd(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = mcgd(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def midpoint(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = midpoint(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def midprice(self, length=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        result = midprice(high=high, low=low, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def ohlc4(self, offset=None, **kwargs):
        open_ = self._get_column(kwargs.pop("open", "open"))
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = ohlc4(open_=open_, high=high, low=low, close=close, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def pwma(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = pwma(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def rma(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = rma(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def sinwma(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = sinwma(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def sma(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = sma(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def ssf(self, length=None, poles=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = ssf(close=close, length=length, poles=poles, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def supertrend(self, length=None, multiplier=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = supertrend(high=high, low=low, close=close, length=length, multiplier=multiplier, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def swma(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = swma(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def t3(self, length=None, a=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = t3(close=close, length=length, a=a, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def tema(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = tema(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def trima(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = trima(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def vidya(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = vidya(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def vwap(self, anchor=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        volume = self._get_column(kwargs.pop("volume", "volume"))

        if not self.datetime_ordered:
            volume.index = self._df.index

        result = vwap(high=high, low=low, close=close, volume=volume, anchor=anchor, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def vwma(self, volume=None, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        volume = self._get_column(kwargs.pop("volume", "volume"))
        result = vwma(close=close, volume=volume, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def wcp(self, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = wcp(high=high, low=low, close=close, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def wma(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = wma(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def zlma(self, length=None, mamode=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = zlma(close=close, length=length, mamode=mamode, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)
    
    # 财务性能指标
    def log_return(self, length=None, cumulative=False, percent=False, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = log_return(close=close, length=length, cumulative=cumulative, percent=percent, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def percent_return(self, length=None, cumulative=False, percent=False, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = percent_return(close=close, length=length, cumulative=cumulative, percent=percent, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)
    
    # 统计指标
    def entropy(self, length=None, base=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = entropy(close=close, length=length, base=base, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def kurtosis(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = kurtosis(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def mad(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = mad(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def median(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = median(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def quantile(self, length=None, q=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = quantile(close=close, length=length, q=q, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def skew(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = skew(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def stdev(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = stdev(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def tos_stdevall(self, length=None, stds=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = tos_stdevall(close=close, length=length, stds=stds, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def variance(self, length=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = variance(close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def zscore(self, length=None, std=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = zscore(close=close, length=length, std=std, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)
    
    # 交易指标
    def adx(self, length=None, lensig=None, mamode=None, scalar=None, drift=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = adx(high=high, low=low, close=close, length=length, lensig=lensig, mamode=mamode, scalar=scalar, drift=drift, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def amat(self, fast=None, slow=None, mamode=None, lookback=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = amat(close=close, fast=fast, slow=slow, mamode=mamode, lookback=lookback, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def aroon(self, length=None, scalar=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        result = aroon(high=high, low=low, length=length, scalar=scalar, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def chop(self, length=None, atr_length=None, scalar=None, drift=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = chop(high=high, low=low, close=close, length=length, atr_length=atr_length, scalar=scalar, drift=drift, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def cksp(self, p=None, x=None, q=None, mamode=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = cksp(high=high, low=low, close=close, p=p, x=x, q=q, mamode=mamode, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def decay(self, length=None, mode=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = decay(close=close, length=length, mode=mode, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def decreasing(self, length=None, strict=None, asint=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = decreasing(close=close, length=length, strict=strict, asint=asint, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def dpo(self, length=None, centered=True, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = dpo(close=close, length=length, centered=centered, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def increasing(self, length=None, strict=None, asint=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = increasing(close=close, length=length, strict=strict, asint=asint, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def long_run(self, fast=None, slow=None, length=None, offset=None, **kwargs):
        if fast is None and slow is None:
            return self._df
        else:
            result = long_run(fast=fast, slow=slow, length=length, offset=offset, **kwargs)
            return self._post_process(result, **kwargs)

    def psar(self, af0=None, af=None, max_af=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", None))
        result = psar(high=high, low=low, close=close, af0=af0, af=af, max_af=max_af, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def qstick(self, length=None, offset=None, **kwargs):
        open_ = self._get_column(kwargs.pop("open", "open"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = qstick(open_=open_, close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def short_run(self, fast=None, slow=None, length=None, offset=None, **kwargs):
        if fast is None and slow is None:
            return self._df
        else:
            result = short_run(fast=fast, slow=slow, length=length, offset=offset, **kwargs)
            return self._post_process(result, **kwargs)

    def supertrend(self, period=None, multiplier=None, mamode=None, drift=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = supertrend(high=high, low=low, close=close, period=period, multiplier=multiplier, mamode=mamode, drift=drift, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def tsignals(self, trend=None, asbool=None, trend_reset=None, trend_offset=None, offset=None, **kwargs):
        if trend is None:
            return self._df
        else:
            result = tsignals(trend, asbool=asbool, trend_offset=trend_offset, trend_reset=trend_reset, offset=offset, **kwargs)
            return self._post_process(result, **kwargs)

    def ttm_trend(self, length=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = ttm_trend(high=high, low=low, close=close, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def vhf(self, length=None, drift=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = vhf(close=close, length=length, drift=drift, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def vortex(self, drift=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = vortex(high=high, low=low, close=close, drift=drift, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def xsignals(self, signal=None, xa=None, xb=None, above=None, long=None, asbool=None, trend_reset=None, trend_offset=None, offset=None, **kwargs):
        if signal is None:
            return self._df
        else:
            result = xsignals(signal=signal, xa=xa, xb=xb, above=above, long=long, asbool=asbool, trend_offset=trend_offset, trend_reset=trend_reset, offset=offset, **kwargs)
            return self._post_process(result, **kwargs)
        
    # 功能函数
    def above(self, asint=True, offset=None, **kwargs):
        a = self._get_column(kwargs.pop("close", "a"))
        b = self._get_column(kwargs.pop("close", "b"))
        result = above(series_a=a, series_b=b, asint=asint, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def above_value(self, value=None, asint=True, offset=None, **kwargs):
        a = self._get_column(kwargs.pop("close", "a"))
        result = above_value(series_a=a, value=value, asint=asint, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def below(self, asint=True, offset=None, **kwargs):
        a = self._get_column(kwargs.pop("close", "a"))
        b = self._get_column(kwargs.pop("close", "b"))
        result = below(series_a=a, series_b=b, asint=asint, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def below_value(self, value=None, asint=True, offset=None, **kwargs):
        a = self._get_column(kwargs.pop("close", "a"))
        result = below_value(series_a=a, value=value, asint=asint, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def cross(self, above=True, asint=True, offset=None, **kwargs):
        a = self._get_column(kwargs.pop("close", "a"))
        b = self._get_column(kwargs.pop("close", "b"))
        result = cross(series_a=a, series_b=b, above=above, asint=asint, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def cross_value(self, value=None, above=True, asint=True, offset=None, **kwargs):
        a = self._get_column(kwargs.pop("close", "a"))
        # a = self._get_column(a, f"{a}")
        result = cross_value(series_a=a, value=value, above=above, asint=asint, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)
    
    # 波动指标
    def aberration(self, length=None, atr_length=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = aberration(high=high, low=low, close=close, length=length, atr_length=atr_length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def accbands(self, length=None, c=None, mamode=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = accbands(high=high, low=low, close=close, length=length, c=c, mamode=mamode, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def atr(self, length=None, mamode=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = atr(high=high, low=low, close=close, length=length, mamode=mamode, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def bbands(self, length=None, std=None, mamode=None, offset=None, **kwargs):
        close  = self._get_column(kwargs.pop("close", "close"))
        result = bbands(close=close, length=length, std=std, mamode=mamode, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def donchian(self, lower_length=None, upper_length=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        result = donchian(high=high, low=low, lower_length=lower_length, upper_length=upper_length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def hwc(self, na=None, nb=None, nc=None, nd=None, scalar=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = hwc(close=close, na=na, nb=nb, nc=nc, nd=nd, scalar=scalar, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def kc(self, length=None, scalar=None, mamode=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = kc(high=high, low=low, close=close, length=length, scalar=scalar, mamode=mamode, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def massi(self, fast=None, slow=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        result = massi(high=high, low=low, fast=fast, slow=slow, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def natr(self, length=None, mamode=None, scalar=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = natr(high=high, low=low, close=close, length=length, mamode=mamode, scalar=scalar, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def pdist(self, drift=None, offset=None, **kwargs):
        open_ = self._get_column(kwargs.pop("open", "open"))
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = pdist(open_=open_, high=high, low=low, close=close, drift=drift, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def rvi(self, length=None, scalar=None, refined=None, thirds=None, mamode=None, drift=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = rvi(high=high, low=low, close=close, length=length, scalar=scalar, refined=refined, thirds=thirds, mamode=mamode, drift=drift, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def thermo(self, long=None, short= None, length=None, mamode=None, drift=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        result = thermo(high=high, low=low, long=long, short=short, length=length, mamode=mamode, drift=drift, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def true_range(self, drift=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        result = true_range(high=high, low=low, close=close, drift=drift, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def ui(self, length=None, scalar=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        result = ui(close=close, length=length, scalar=scalar, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)
    

    # 交易量指标
    def ad(self, open_=None, signed=True, offset=None, **kwargs):
        if open_ is not None:
            open_ = self._get_column(kwargs.pop("open", "open"))
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        volume = self._get_column(kwargs.pop("volume", "volume"))
        result = ad(high=high, low=low, close=close, volume=volume, open_=open_, signed=signed, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def adosc(self, open_=None, fast=None, slow=None, signed=True, offset=None, **kwargs):
        if open_ is not None:
            open_ = self._get_column(kwargs.pop("open", "open"))
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        volume = self._get_column(kwargs.pop("volume", "volume"))
        result = adosc(high=high, low=low, close=close, volume=volume, open_=open_, fast=fast, slow=slow, signed=signed, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def aobv(self, fast=None, slow=None, mamode=None, max_lookback=None, min_lookback=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        volume = self._get_column(kwargs.pop("volume", "volume"))
        result = aobv(close=close, volume=volume, fast=fast, slow=slow, mamode=mamode, max_lookback=max_lookback, min_lookback=min_lookback, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def cmf(self, open_=None, length=None, offset=None, **kwargs):
        if open_ is not None:
            open_ = self._get_column(kwargs.pop("open", "open"))
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        volume = self._get_column(kwargs.pop("volume", "volume"))
        result = cmf(high=high, low=low, close=close, volume=volume, open_=open_, length=length, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def efi(self, length=None, mamode=None, offset=None, drift=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        volume = self._get_column(kwargs.pop("volume", "volume"))
        result = efi(close=close, volume=volume, length=length, offset=offset, mamode=mamode, drift=drift, **kwargs)
        return self._post_process(result, **kwargs)

    def eom(self, length=None, divisor=None, offset=None, drift=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        volume = self._get_column(kwargs.pop("volume", "volume"))
        result = eom(high=high, low=low, close=close, volume=volume, length=length, divisor=divisor, offset=offset, drift=drift, **kwargs)
        return self._post_process(result, **kwargs)

    def kvo(self, fast=None, slow=None, length_sig=None, mamode=None, offset=None, drift=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        volume = self._get_column(kwargs.pop("volume", "volume"))
        result = kvo(high=high, low=low, close=close, volume=volume, fast=fast, slow=slow, length_sig=length_sig, mamode=mamode, offset=offset, drift=drift, **kwargs)
        return self._post_process(result, **kwargs)

    def mfi(self, length=None, drift=None, offset=None, **kwargs):
        high = self._get_column(kwargs.pop("high", "high"))
        low = self._get_column(kwargs.pop("low", "low"))
        close = self._get_column(kwargs.pop("close", "close"))
        volume = self._get_column(kwargs.pop("volume", "volume"))
        result = mfi(high=high, low=low, close=close, volume=volume, length=length, drift=drift, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def nvi(self, length=None, initial=None, signed=True, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        volume = self._get_column(kwargs.pop("volume", "volume"))
        result = nvi(close=close, volume=volume, length=length, initial=initial, signed=signed, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def obv(self, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        volume = self._get_column(kwargs.pop("volume", "volume"))
        result = obv(close=close, volume=volume, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def pvi(self, length=None, initial=None, signed=True, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        volume = self._get_column(kwargs.pop("volume", "volume"))
        result = pvi(close=close, volume=volume, length=length, initial=initial, signed=signed, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def pvol(self, volume=None, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        volume = self._get_column(kwargs.pop("volume", "volume"))
        result = pvol(close=close, volume=volume, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def pvr(self, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        volume = self._get_column(kwargs.pop("volume", "volume"))
        result = pvr(close=close, volume=volume)
        return self._post_process(result, **kwargs)

    def pvt(self, offset=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        volume = self._get_column(kwargs.pop("volume", "volume"))
        result = pvt(close=close, volume=volume, offset=offset, **kwargs)
        return self._post_process(result, **kwargs)

    def vp(self, width=None, percent=None, **kwargs):
        close = self._get_column(kwargs.pop("close", "close"))
        volume = self._get_column(kwargs.pop("volume", "volume"))
        result = vp(close=close, volume=volume, width=width, percent=percent, **kwargs)
        return self._post_process(result, **kwargs)