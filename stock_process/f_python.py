import functools

# 使用 reduce 函数计算 5！
import operator

res = functools.reduce(lambda a, b: a*b, range(1, 6))
# print(res)

# 计算 0-5 的累计异或
n = 0
for i in range(1, 6):
    n ^= i
# print(n)

res = functools.reduce(lambda a, b: a ^ b, range(6))
# print(res)


# temp test
last = [23414, 23401, 23447, 23485, 23466, 23406, 23367, 23362, 23380, 23366, 23362, 23325, 23299,
        23342, 23338, 23340, 23339, 23243, 23207, 23222, 23232, 23231, 23218, 23222, 23230, 23227,
        23184]
h3 = functools.reduce(operator.add, last[:3]) / len(last[:3])

temp = [h3] + last[3:]
ret = zip(*[iter(temp)]*2)


def gen_H():
    for (x, y) in ret:
        print(x, y)
        yield x+y




