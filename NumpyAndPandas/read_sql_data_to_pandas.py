import time

from sqlalchemy import create_engine
import pandas as pd


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


@log_method_time_usage
def gen_csv(conf, table):

    mysql_string = f"mysql+pymysql://{conf['user']}:{conf['password']}@{conf['host']}:\
    {conf.get('port')}/{conf['sqlDBname']}?charset=gbk"

    DATACENTER = create_engine(mysql_string)

    # query = f"select * from {db}.{table} where id > {start} and id <= {end};"

    # 获取所有的 ids
    # db.execute("create table users(userid char(10), username char(50))")
    min_id = DATACENTER.execute(f"select min(id) from {table};").first()[0]
    print(min_id)

    max_id = DATACENTER.execute(f"select max(id) from {table};").first()[0]
    print(max_id)

    # import sys
    # sys.exit(0)
    file = None

    start = min_id

    while start <= max_id:

        query = f"select id from {table} where id >={start} and id <{start+50000} order by id asc;"

        data = pd.read_sql(query, DATACENTER)

        file = f"{conf['sqlDBname']}_{table}.csv"

        data.to_csv(file, index=0, mode="a")

        start += 50000

    return file


if __name__ == "__main__":

    # host = "139.159.176.118"
    # port = 3306
    # user = "dcr"
    # password = "acBWtXqmj2cNrHzrWTAciuxLJEreb*4EgK4"
    # sqlDBname = "datacenter"
    # mongoDBname = "JQdata"

    cf = {
        "host": "139.159.176.118",
        "port": 3306,
        "user": "dcr",
        "password": "acBWtXqmj2cNrHzrWTAciuxLJEreb*4EgK4",
        "sqlDBname": "datacenter",
        # "mongoDBname": "JQdata",
    }
    table = "index_indexcomponentsweight"
    gen_csv(cf, table)
