import abc
import datetime

import numpy as np
from enum import Enum, auto


class FactorType(Enum):
    """枚举实例"""

    OPEN = "开盘价"
    HIGH = "最高价"
    LOW = "最低价"
    CLOSE = "收盘价"
    VOLUME = "成交量"
    AMOUNT = "成交额"

    # 测试因子
    TESTFACTOR = "测试因子"


Ft = FactorType


class Factor(object):
    """因子类"""

    def __init__(self, factor_type: FactorType, params: list = None, **kwargs):
        self.type = factor_type
        self.params = params or []
        self._kwargs = kwargs

    def __str__(self):
        return f"{self.type}:{self.params}"

    def __repr__(self):
        return f"{self.type}:{self.params}"


class Singleton(abc.ABCMeta):
    """单例元类"""
    # 确保某一个类只有一个实例存在 继承该类这个类就只会被创建一次

    _instance = dict()

    def __call__(cls, *args, **kwargs):
        meta = cls.__class__
        if cls not in meta._instance:
            meta._instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return meta._instance[cls]


class AbstractTrident(abc.ABC):
    """定义了 Trident 要实现的接口"""

    @abc.abstractmethod
    def fixed_factor(self, factor: Factor, instruments: list, start_time: datetime, end_time: datetime,
                     fqc=None, output: np.ndarray = None) -> np.ndarray:

        raise NotImplementedError

    @abc.abstractmethod
    def fixed_time(self, time: datetime, insturments: list, factors: list,
                   fqc=None, output: np.ndarray = None) -> np.ndarray:

        raise NotImplementedError

    @abc.abstractmethod
    def fixed_symbol(self, instrument: str, factors: list, start_time: datetime, end_time: datetime,
                     fqc=None, output: np.ndarray = None) -> np.ndarray:

        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_instance(cls):

        raise NotImplementedError


_factor_tridents = {

}


def handle_factor(*factor_types: FactorType):
    """
    类装饰器，使用该装饰器的类必须实现AbstractTrident
    :param factor_types:
    :return:
    """
    def wrapper(klass):
        if not issubclass(klass, AbstractTrident):
            raise TypeError(f"class {klass.__name__} doesn't implement AbstractTrident")
        for ft in factor_types:
            if not isinstance(ft, FactorType):
                raise ValueError(f"{ft} is not a valid FactorType")
            # 在 _factor_tridents 里面寻找对应的处理器
            existed = _factor_tridents.get(ft)
            if existed is not None:  # 一个因子只能注册在一个处理器里面
                raise ValueError(f"a trident {existed.__name__} already registered for factor {ft}")
            _factor_tridents[ft] = klass  # 注册过程
        return klass
    return wrapper


def get_factor_handler(ft: FactorType) -> AbstractTrident:
    """
    根据传入的FactorType返回对应的处理器
    :param ft:
    :return:
    """
    return _factor_tridents.get(ft)


_shares = dict()


def _handle(f_type):
    """装饰器 将某个因子以及对应的处理方法注册到 share 中去"""
    def wrapper(method):
        _shares[f_type] = method

        def wrapped(self, *args, **kwargs):
            return method(self, *args, **kwargs)
        return wrapped
    return wrapper


@handle_factor(Ft.TESTFACTOR)
class KlineFinance(AbstractTrident, metaclass=Singleton):
    """继承抽象接口;  单例"""

    _shares = {

    }

    @classmethod
    def get_instance(cls):

        pass

    def __init__(self, *args, **kwargs):
        # super(KlineFinance, self).__init__(*args, **kwargs)
        # self._calendar = TradeCalendar()
        # self._factor = None
        pass

    # @property
    # def trident(self):
    #     # 返回环境中的一个 Trident 实例对象
    #     # return Environment.get_instance().mod_dict["trident"]
    #     pass

    def fixed_factor(self, factor: Factor, instruments,  start_time,  end_time, fqc=None, output: np.ndarray = None):

        # if output is None:
        #     dtyps = [("date", "uint64")]
        #     for code in instruments:
        #         dtyps.append((code, "?"))
        #
        #     # todo: calendar 要支持不同的频率
        #     # 现在的 calendar 只支持交易日频率 ...
        #     calendar = self._calendar.calendar(start_time, end_time)
        #     output = np.full((calendar.shape[0],), np.NAN, dtype=dtyps)
        #     output["date"] = calendar

        # 给某个因子找到处理的注册方法 ...
        # 这个因子必须是枚举类型 然后在方法的 装饰器 中进行了注册 ..
        method = _shares.get(factor.type)
        print(method)

        if method is None:  # 注册未实现
            raise ValueError(f"factor {factor} registered but not implemented.")

        # 返回使用该方法处理的结果
        # 所以每个具体的实现方法里面的参数就是： （1） 合约代码； （2） 开始时间； （3）结束时间
        # （TODO）使用 method 处理就是为了填充 output ？？
        method(instruments, start_time, end_time, output)

        # return output

    def fixed_time(self, time: datetime, insturments: list, factors: list,
                   fqc=None, output: np.ndarray = None) -> np.ndarray:
        pass

    def fixed_symbol(self, instrument: str, factors: list, start_time: datetime, end_time: datetime,
                     fqc=None, output: np.ndarray = None) -> np.ndarray:
        pass

    @_handle(Ft.TESTFACTOR)
    def process_test(self, instruments, start_time, end_time, output=None):
        print(instruments)
        print(start_time)
        print(end_time)
        print(output)


if __name__ == "__main__":
    # kf = KlineFinance(1, 2)
    # kf = KlineFinance(3, 4)
    # kf.test_ab()
    # print(KlineFinance._instance)

    # 是否进行了注册
    # print(_factor_tridents)

    # 方法是否进行了注册
    print(_shares)

    # 类内部的 字典 有啥作用 还是空的啊 ...
    # print(KlineFinance._shares)

    # 测试 fixed_factor ...
    # codes = ["a", "b", "c"]
    # start = datetime.datetime(2000, 1, 1)
    # end = datetime.datetime(2019, 1, 1)
    # f = Factor(Ft.TESTFACTOR)
    # KlineFinance().fixed_factor(f, codes, start, end, None, None)

    print(_factor_tridents)

    pass
