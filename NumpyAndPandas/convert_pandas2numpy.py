# Convert DataFrame to a NumPy record array.

# Index will be put in the 'index' field of the record array if requested.

"""
Parameters
    ----------
    index : boolean, default True
        Include index in resulting record array, stored in 'index' field.
    convert_datetime64 : boolean, default None
        .. deprecated:: 0.23.0

        Whether to convert the index to datetime.datetime if it is a
        DatetimeIndex.

    Returns
    -------
    y : numpy.recarray

    See Also
    --------
    DataFrame.from_records: convert structured or record ndarray
        to DataFrame.
    numpy.recarray: ndarray that allows field access using
        attributes, analogous to typed columns in a
        spreadsheet.
"""
import sys
import datetime
import pandas as pd
import numpy as np

df = pd.DataFrame({'A': [1, 2], 'B': [0.5, 0.75]}, index=['a', 'b'])
print(df)
print(df.index.tolist())
sys.exit(0)
"""
   A     B
a  1  0.50
b  2  0.75
"""
ret1 = df.to_records()
print(ret1)
"""
rec.array([('a', 1, 0.5 ), ('b', 2, 0.75)],
          dtype=[('index', 'O'), ('A', '<i8'), ('B', '<f8')])
"""
# By default, timestamps are converted to `datetime.datetime`
df.index = pd.date_range('2018-01-01 09:00', periods=2, freq='min')
print(df)
"""
                     A     B
2018-01-01 09:00:00  1  0.50
2018-01-01 09:01:00  2  0.75
"""
print(df.to_records())
"""
rec.array([('2018-01-01T09:00:00.000000000', 1, 0.5 ),
           ('2018-01-01T09:01:00.000000000', 2, 0.75)],
          dtype=[('index', '<M8[ns]'), ('A', '<i8'), ('B', '<f8')])
"""

# The timestamp conversion can be disabled so NumPy's datetime64 data type is used instead
print(df.to_records(convert_datetime64=False))
"""
rec.array([('2018-01-01T09:00:00.000000000', 1, 0.5 ),
           ('2018-01-01T09:01:00.000000000', 2, 0.75)],
          dtype=[('index', '<M8[ns]'), ('A', '<i8'), ('B', '<f8')])
"""


# 将 index 设置为精确到 s 的时间戳格式
def yyyymmddhhmmss(d: datetime.datetime) -> int:
    """
    datetime to its int reprsentation. e.g. datetime(2018, 01, 02, 03, 45, 56) - > 20180102034556
    :param d:
    :return:
    """
    return d.second + d.minute * 100 + d.hour * 10 ** 4 + d.day * 10 ** 6 + d.month * 10 ** 8 + d.year * 10 ** 10

