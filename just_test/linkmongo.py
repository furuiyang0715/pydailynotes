import time
import datetime
import pprint
import sys

import pandas as pd
import numpy as np
from pymongo import MongoClient

cld = MongoClient("127.0.0.1:27017")

# Ft.TOTALOPERATINGCOST: ("comcn_incomestatement", "TotalOperatingCost"),  # 营业总成本
# Ft.TOTALOPERATINGREVENUE: ("comcn_incomestatement", "TotalOperatingRevenue"),  # 营业总收入
# Ft.TOTALASSETS: ("comcn_balancesheet", "TotalAssets"),  # 资产总计(元)
coll_map = {
    "TotalOperatingRevenue": "comcn_incomestatement",
    "TotalOperatingCost": "comcn_incomestatement",
    "TotalAssets": "comcn_balancesheet",
}


def log_method_time_usage(func):
    def wrapped(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        # system_log.info(f"[TimeUsage] {func.__module__}.{func.__name__} usage: {time.time()-start}")
        dt = time.time()-start
        if dt > 0.1:
            print(f"[TimeUsage] {func.__module__}.{func.__name__} usage: {dt}")
        return result
    return wrapped


def gen_all_quarters(start: datetime.datetime, end: datetime.datetime):
    idx = pd.date_range(start=start, end=end, freq="Q")
    # dt_list = [dt.strftime("%Y-%m-%d %H:%M:%S") for dt in idx]
    dt_list = [dt.to_pydatetime() for dt in idx]
    return dt_list


def gen_dfs(instruments, fields, operator=None):
    # operator 是输入的几个字段之间的关系 例如operator是 "+", 说明输入的几个字段是连续加的关系
    # 且这几个字段是来自于同一张表
    # 这里想到了两种的处理方式（1） 做成生成器的形式 每次 yield 出 pivot_table 的一个的结果 但是查询过程只进行一次
    # （2）另外一种是不显示中间结果 直接根据输入的运算符计算最终值

    coll_name = coll_map.get(fields[0])
    coll = cld.JQdata[coll_name]

    groupby = ["SecuCode", "EndDate"]  # 按照合约季度节点以及字段去分组
    # groupby.extend(fields)

    group = {
        # _id 表征了这个分组的唯一主键
        '_id': {key: ('$%s' % key) for key in groupby} or {'None': '$None'},
        # 剩下的字段表明了在主键完全相同的情况 其余的字段的取值情况 这些字段不一定在同一个文档中获得
        "PubDate": {"$last": "$PubDate"},
        "EndDate": {"$last": "$EndDate"},
        "SecuCode": {"$last": "$SecuCode"},


    }
    start_time = datetime.datetime(2011, 1, 1)
    end_time = datetime.datetime(2013, 1, 1)
    quarter_list = gen_all_quarters(start_time, end_time)
    try:
        ret1 = list(coll.aggregate(
            [{'$match': {'SecuCode': {'$in': instruments},
                         'EndDate': {'$in': quarter_list}}},
             {'$group': group}]))
    except Exception as e:
        raise

    # 只需要 ret 中的 _id 字段
    ret1 = [r.get("_id") for r in ret1]

    df = pd.DataFrame(data=ret1)

    # 在 drop column 之前需要确保非空
    if df.empty:
        print("没有查询该合约的相关数据")
    else:
        pass

    df = df.fillna(0)  # 防止如果 df 中的 field 值全部为 None 的话 pivot_table 会报错
    # for i in range(len(fields)):
    #     yield (fields[i], df.pivot_table(index='EndDate', columns='SecuCode', values=fields[i]))

    df1 = df.pivot_table(index='EndDate', columns='SecuCode', values=fields[0])
    # df2 = df.pivot_table(index='EndDate', columns='SecuCode', values=fields[1])
    # return df1, df2
    return df1


def gen_df(instruments, field):
    coll_name = coll_map.get(field)
    coll = cld.JQdata[coll_name]
    groupby = ["SecuCode", "EndDate"]  # 按照合约季度节点以及字段去分组
    group = {
     '_id': {key: ('$%s' % key) for key in groupby} or {'None': '$None'},
     field: {"$last": "$" + field},
     "PubDate": {"$last": "$PubDate"},
     "EndDate": {"$last": "$EndDate"},
     "SecuCode": {"$last": "$SecuCode"},
    }
    start_time = datetime.datetime(2011, 1, 1)
    end_time = datetime.datetime(2013, 1, 1)
    quarter_list = gen_all_quarters(start_time, end_time)
    try:
        ret1 = list(coll.aggregate(
         [{'$match': {'SecuCode': {'$in': instruments},
                      'EndDate': {'$in': quarter_list}}},
          {'$group': group}]))
    except Exception as e:
        raise
    # convert ret1 to df
    df = pd.DataFrame(data=ret1)
    # 在 drop column 之前需要确保非空
    if df.empty:
        print("没有查询该合约的相关数据")
    else:
        # print(df)
        pass
    df = df.drop(columns=["_id", "PubDate"])
    # print(df)
    df = df.fillna(0)  # 防止如果 df 中的 field 值全部为 None 的话 pivot_table 会报错
    # 将 instruments 转到 columns 上
    df1 = df.pivot_table(index='EndDate', columns='SecuCode', values=field)
    return df1


@log_method_time_usage
def m1(instruments, fields):
    df1 = gen_df(instruments, fields[0])
    print(df1)
    # df2 = gen_df(instruments, fields[1])
    # df = df1 + df2
    # return df


@log_method_time_usage
def m2(instruments, fields):
    df1 = gen_dfs(instruments, fields)
    print(df1)
    # df1, df2 = gen_dfs(instruments, fields)
    # print(df1)
    # df = df1 + df2
    # return df


if __name__ == "__main__":
    codes = ["000585.XSHE", "600084.XSHG", "600328.XSHG", "600432.XSHG"]
    fs = ["TotalOperatingRevenue",
          # "TotalOperatingCost",
          ]
    m1(codes, fs)

    print()
    print()
    print()

    m2(codes, fs)




