import pymongo
import os


class NONESENSE:
    mongocli = pymongo.MongoClient(os.environ.get("JZDATAURI", "mongodb://127.0.0.1:27017"))


def DB() -> pymongo.MongoClient:
    return NONESENSE.mongocli


db = DB()
