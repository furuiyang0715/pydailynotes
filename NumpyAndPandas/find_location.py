import datetime
import pprint

import numpy as np


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


if __name__ == "__main__":
    start = datetime.datetime(2013, 1, 1)
    end = datetime.datetime(2017, 3, 4)
    res = gen_complete_days(start, end)
    print(pprint.pformat(res))
    someday = yyyymmdd_date(datetime.datetime(2013, 1, 2))  # 1
    location = find_date_in_array(someday, res)
    print(location)

