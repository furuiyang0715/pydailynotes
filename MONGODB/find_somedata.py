import datetime

from MONGODB.create_connection import DB

SOFT_BASE_COL = "soft_base"
BIG_FINANCE_COL = "big_finance"

client = DB()
# 数据库
_db = client['stock']

# 集合
soft_collection = getattr(_db, SOFT_BASE_COL)
big_collection = getattr(_db, BIG_FINANCE_COL)

code = "SZ300367"
date = datetime.datetime(2019, 4, 27)

base_finance = soft_collection.find(
            {"code": code, "time": {"$lte": date}}, {"code": 0, "_id": 0}) \
            .sort('time', -1).limit(1)

