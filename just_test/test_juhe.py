import datetime
import pprint
import pandas as pd
from pymongo import MongoClient

cld = MongoClient("127.0.0.1:27017")

# data1 = {
#     "EndDate": datetime.datetime(2001, 3, 31),
#     "PubDate": datetime.datetime(2000, 1, 1),
#     "value": 2000,
#     "value2": 1111,
#     "SecuCode": "000001",
# }
#
#
# data2 = {
#     "EndDate": datetime.datetime(2001, 3, 31),
#     "PubDate": datetime.datetime(2000, 2, 1),
#     "value": 1000,
#     "value2": 2222,
#     "SecuCode": "000001",
# }
#
# data4 = {
#     "EndDate": datetime.datetime(2001, 6, 30),
#     "PubDate": datetime.datetime(2000, 6, 1),
#     "value": 5000,
#     "value2": 4444,
#     "SecuCode": "000001",
# }
#
# data3 = {
#     "EndDate": datetime.datetime(2001, 6, 30),
#     "PubDate": datetime.datetime(2000, 4, 1),
#     "value": 6000,
#     "value2": 3333,
#     "SecuCode": "000001",
# }

# 插入另外一个股票的test数据

data1 = {
    "EndDate": datetime.datetime(2010, 3, 31),
    "PubDate": datetime.datetime(2000, 1, 1),
    "value": 2000,
    "value2": 1111,
    "SecuCode": "000002",
}


data2 = {
    "EndDate": datetime.datetime(2010, 3, 31),
    "PubDate": datetime.datetime(2000, 2, 1),
    "value": 1000,
    "value2": 2222,
    "SecuCode": "000002",
}

data4 = {
    "EndDate": datetime.datetime(2010, 6, 30),
    "PubDate": datetime.datetime(2000, 6, 1),
    "value": 5000,
    "value2": 4444,
    "SecuCode": "000002",
}

data3 = {
    "EndDate": datetime.datetime(2010, 6, 30),
    "PubDate": datetime.datetime(2000, 4, 1),
    "value": 6000,
    "value2": 3333,
    "SecuCode": "000002",
}

datas = [data1, data2, data4, data3]

# data2 以及 data4  1000 和 5000

# res = cld.justtest.test.delete_many({"SecuCode": "000001"})
# print(res)

# res = cld.justtest.test.insert_many(datas)
# print(res)


def gen_all_quarters(start: datetime.datetime, end: datetime.datetime):
    idx = pd.date_range(start=start, end=end, freq="Q")
    # dt_list = [dt.strftime("%Y-%m-%d %H:%M:%S") for dt in idx]
    dt_list = [dt.to_pydatetime() for dt in idx]
    return dt_list


# groupby = ["SecuCode", "EndDate"]
# field = "value"
# group = {
#  '_id': {key: ('$%s' % key) for key in groupby} or {'None': '$None'},
#  field: {"$last": "$" + field},
#  "PubDate": {"$last": "$PubDate"},
#  "EndDate": {"$last": "$EndDate"},
#  "SecuCode": {"$last": "$SecuCode"},
# }
# start_time = datetime.datetime(2000, 1, 1)
# end_time = datetime.datetime(2002, 1, 1)
# quarter_list = gen_all_quarters(start_time, end_time)
# try:
#     ret1 = list(cld.justtest.test.aggregate(
#      [{'$match': {'SecuCode': {'$in': ["000001"]},
#                   'EndDate': {'$in': quarter_list}}},
#       {'$group': group}]))
# except Exception as e:
#     raise
# # convert ret1 to df
# df = pd.DataFrame(data=ret1)
#
# # 在 drop column 之前需要确保非空
# if df.empty:
#     print("没有查询该合约的相关数据")
# else:
#     # print(df)
#     pass
# df = df.drop(columns=["_id", "PubDate"])
# print(df)



# groupby = ["SecuCode", "EndDate"]  # 按照合约季度节点以及字段去分组
# groupby.extend(["value"])
# print(groupby)
# group = {
#     '_id': {key: ('$%s' % key) for key in groupby} or {'None': '$None'},
#     "PubDate": {"$last": "$PubDate"},
#     # "EndDate": {"$last": "$EndDate"},
#     # "SecuCode": {"$last": "$SecuCode"},
# }
# start_time = datetime.datetime(2000, 1, 1)
# end_time = datetime.datetime(2002, 1, 1)
# quarter_list = gen_all_quarters(start_time, end_time)
# try:
#     ret1 = list(cld.justtest.test.aggregate(
#         [{'$match': {'SecuCode': {'$in': ['000001']},
#                      'EndDate': {'$in': quarter_list}}},
#          {'$group': group}]))
# except Exception as e:
#     raise
# ret1 = [r.get("_id") for r in ret1]
# print(pprint.pformat(ret1))
# df = pd.DataFrame(data=ret1)
# print(df)


groupby = ["SecuCode", "EndDate"]
start_time = datetime.datetime(2000, 1, 1)
end_time = datetime.datetime(2019, 1, 1)
quarter_list = gen_all_quarters(start_time, end_time)

ret1 = list(cld.justtest.test.find({'SecuCode': {'$in': ["000001", "000002"]},
                                    'EndDate': {'$in': quarter_list}
                                    }))
print(pprint.pformat(ret1))
df1 = pd.DataFrame(data=ret1)
# print(df1)
df2 = df1.drop(columns=["_id"])
print(df2)
print()

# df.sort_values(by="sales" , ascending=False) by 指定列 ascending

# 按照从大到小的顺序排列
df3 = df2.sort_values(by="PubDate", ascending=False)
print(df3)
print()

# 按照 EndDate 去重 保留第一个出现的数据
df4 = df3.drop_duplicates(["EndDate", "SecuCode"])
print(df4)
print()







