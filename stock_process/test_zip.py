# 测试 zip 的使用
ll = list(range(10))
print(ll)

# 将相邻两个数字进行打包
ret1 = zip(*[iter(ll)]*2)
print(list(ret1))

# 将相邻3个数字进行打包 不够的将不被列出
ret2 = zip(*[iter(ll)]*3)
print(list(ret2))

# 能够这样做的原因是生成的三个迭代器实质上是同一个迭代器
print([iter(ll)]*3)
# [<list_iterator object at 0x10da1be48>, <list_iterator object at 0x10da1be48>,
# <list_iterator object at 0x10da1be48>]


# 实现一个函数 输入列表以及分组的个数，生成分组数据
group_adjacent = lambda a, k: zip(*([iter(a)] * k))

# 调用
print(list(group_adjacent(ll, 3)))


### 现在想要的效果是每个值是相邻的累加
# 例如输入的是 [0, 1,  2,    3,     4,       5, 6, 7, 8, 9]
# 输出的是    [0, 0.5, 1.25, 2.125, 3.0625, ... ]

# 通过数学的方法计算出的推导公式是 : suanfa.jpg





