### 创建数据库 
use runoob 

注意， 集合只有在内容插入后才会创建! 就是说，创建集合(数据表)后要再插入一个文档(记录)，集合才会真正创建

### 查看所有的数据库 
show dbs

### 删除数据库
db.dropDatabase()
会删除当前的数据库，默认是 test，我们可以使用 db 命令来查看当前的数据库名。

### 创建一个集合 
db.createCollection("mycoll")
创建集合时可以指定有关内存的大小以及索引的选择项

### 创建固定集合
db.createCollection("mycol", { capped : true, autoIndexId : true, size : 6142800, max : 10000 } )
创建固定集合 mycol, 整个集合的空间大小是 6142800 KB，文档最大个数为 10000 个。
在 mongodb 中，一般我们不需要创建集合，在我们插入文档的时候，MongoDB 会自动创建集合。

### 查看所有的集合
show tables

### 删除集合 
db.mycoll.drop()

### insert 插入一条数据
mongo 中默认的数据库是 test，如果我们没有创建数据库，默认的数据会放到 test 集合中去。
db.mycoll.insert({"name": "ruiyang"})

我们也可以首先定义一个变量，然后将其插入集合：
document = ({"name": "ruiyang", "age": 24})
db.mycoll.insert(document)

#### save 插入或者更新一条数据 
我们也可以使用 save() 方法，如果指定 _id 字段， save 等同于 insert，指定 _id 则相当于替换。


#### 