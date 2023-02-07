import datetime
import numpy as np


def yyyymmdd_date(dt: datetime) -> int:
    """
    将 datetime 转化为 int
    :param dt:
    :return:
    """
    return dt.year * 10000 + dt.month * 100 + dt.day


def get_one_day(begin_date, days):
    day = datetime.timedelta(days=1)
    for i in range(days):
        yield begin_date + day*i


def gen_complete_days(start: datetime.datetime, end: datetime.datetime):
    """
    生成起止日期之间的所有自然日
    :param start:
    :param end:
    :return:
    """

    dates_list = list()
    for date in get_one_day(start, (end-start).days):
        dates_list.append(yyyymmdd_date(date))
    return np.array(dates_list)


def avg_datetime(*dts: datetime) -> datetime:
    """
    计算一组时间的平均值
    :param dts:
    :return:
    """
    avg_ts = sum(map(lambda x: x.timestamp(), dts)) / len(dts)
    return datetime.datetime.fromtimestamp(avg_ts)


def find_date_in_array(dt: str, array: "numpy.ndarray") -> int:
    """
    找到某个元素在ndarray中的位置
    :param dt:
    :param array:
    :return:
    """
    for i, d in enumerate(array):
        if d == dt:
            return i
    return -1
