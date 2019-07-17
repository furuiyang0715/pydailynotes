from kazoo.client import KazooClient

zk = KazooClient(hosts='127.0.0.1:2181')

# 启动连接
zk.start()

# 停止连接
# zk.stop()


# 创建节点路径，但不能设置节点数据值
zk.ensure_path("/my/favorite")

# 创建节点，并设置节点保存数据，ephemeral表示是否是临时节点，sequence表示是否是顺序节点
zk.create("/my/favorite/node", b"a value", ephemeral=True, sequence=True)

# 获取子节点列表
children = zk.get_children("/my/favorite")

print(children)

# 获取节点数据data 和节点状态stat
data, stat = zk.get("/my/favorite")
# data, stat = zk.get(children[0])

print(data)

print(stat)


def my_func(event):
    # 检查最新的节点数据
    pass

# 当子节点发生变化的时候，调用my_func
children = zk.get_children("/my/favorite/node", watch=my_func)
