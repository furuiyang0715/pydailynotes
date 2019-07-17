# MongoJStrategy.update(id, {"$push": {"task_names": task_name}}
# 主要测试一下这句话 push 进去的结构是放在列表的哪个位置

import pymongo
cld = pymongo.MongoClient("127.0.0.1:27017")
data = {
    "user": "furuiyang",
    "ll": []
}
# cld.mytest.pushtest.insert(data)

print(cld.mytest.pushtest.find({"user": "furuiyang"}).next())

cld.mytest.pushtest.update_many({"user": "furuiyang"}, {"$push": {"ll": "000004"}})
# cld.mytest.pushtest.update_many({"user": "furuiyang"}, {"$push": {"ll": "000002"}})
# cld.mytest.pushtest.update_many({"user": "furuiyang"}, {"$push": {"ll": "000003"}})

print(cld.mytest.pushtest.find({"user": "furuiyang"}).next())

