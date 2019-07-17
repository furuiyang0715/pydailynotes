# 从 mongodb 数据库直接读取数据到 pandas 中

import pymongo

import pandas as pd

client = pymongo.MongoClient('localhost', 27017)
db = client['JQdata']
index = db['index_indexcomponentsweight']

data = pd.DataFrame(list(index.find()))

# 删除其中的 _id 字段
