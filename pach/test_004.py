import sys

# import pymysql
#
# db = pymysql.connect(host='localhost',user='root', password='ruiyang', port=3306)
# cursor = db.cursor()
# cursor.execute('SELECT VERSION()')
# data = cursor.fetchone()
# print('Database version:', data)
# cursor.execute("CREATE DATABASE spiders DEFAULT CHARACTER SET utf8")
# db.close()


# import pymysql
#
# db = pymysql.connect(host='localhost', user='root', password='ruiyang', port=3306, db='spiders')
# cursor = db.cursor()
# sql = 'CREATE TABLE IF NOT EXISTS students (id VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, age INT NOT NULL, PRIMARY KEY (id))'
# cursor.execute(sql)
# db.close()


import pymysql
#
# id = '20120001'
# user = 'Bob'
# age = 20
#
db = pymysql.connect(host='localhost', user='root', password='ruiyang', port=3306, db='spiders')
cursor = db.cursor()
# sql = 'INSERT INTO students(id, name, age) values(%s, %s, %s)'
# try:
#     cursor.execute(sql, (id, user, age))
#     db.commit()
# except:
#     db.rollback()
# db.close()


# data = {
#     'id': '20120002',
#     'name': 'Bob',
#     'age': 20
# }
# table = 'students'
# keys = ', '.join(data.keys())
# values = ', '.join(['%s'] * len(data))
# sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
# try:
#    if cursor.execute(sql, tuple(data.values())):
#        print('Successful')
#        db.commit()
# except Exception as e:
#     print('Failed')
#     print(e)
#     db.rollback()
# db.close()


data = {
    'id': '20120001',
    'name': 'Bob',
    'age': 21
}

table = 'students'
keys = ', '.join(data.keys())
values = ', '.join(['%s'] * len(data))

# 在后面加了 ON DUPLICATE KEY UPDATE，这个的意思是如果主键已经存在了，那就执行更新操作，
# 比如在这里我们传入的数据 id 仍然为 20120001，但是年龄有所变化，由 20 变成了 21，但在这条数据不会被插入，而是将 id 为 20120001 的数据更新。


sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys, values=values)
update = ','.join([" {key} = %s".format(key=key) for key in data])
sql += update
# print(sql)
#
# print(tuple(data.values())*2)
#
# print(tuple(data.values()))

# sys.exit(0)

try:
    if cursor.execute(sql, tuple(data.values())*2):
        print('Successful')
        db.commit()
except:
    print('Failed')
    db.rollback()
db.close()