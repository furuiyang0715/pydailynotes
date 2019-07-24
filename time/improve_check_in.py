#### 链接： https://mp.weixin.qq.com/s/ml7W3GVeG84gQ8i2TguOuQ
### 加速查找

#### 使用 set 而不是 list 进行查找

# from timeit import timeit
#
# data = (i**2 for i in range(10**6))
#
# list_data = lambda data: list(data)
# set_data = lambda data: set(data)
#
# ret1 = timeit("list_data(data)", globals={"list_data": list_data, "data": data}, number=100)
# print(ret1)  # 0.350903796
#
# ret2 = timeit("set_data(data)", globals={"set_data": set_data, "data": data}, number=100)
# print(ret2)  # 2.4346000000008416e-05
#
# print(ret1 / ret2)  # 14413.20118294088



#### 使用 dict 而不是两个 list 进行匹配查找

# from timeit import timeit
#
# list_a = [2**i-1 for i in range(10**3)]
# print(list_a)
# list_b = [i**2 for i in list_a]
# dict_ab = dict(zip(list_a, list_b))
#
# list_find_b = lambda x: list_b[list_a.index(x)]
# dict_find_b = lambda x: dict_ab.get(x, None)
#
# ret1 = timeit("list_find_b(x)", globals={"list_find_b": list_find_b, "x": 65535}, number=100)
# ret2 = timeit("dict_find_b(x)", globals={"dict_find_b": dict_find_b, "x": 65535}, number=100)
# print(ret1 / ret2)


### 加速循环
#### 优先使用 for 循环而不是 while 循环

# from timeit import timeit
#
#
# def test_while_loop():
#     s, i = 0, 0
#     while i < 10000:
#         i += 1
#         s += i
#     # print(s)
#
#
# def test_for_loop():
#     s = 0
#     for i in range(10000):
#         i += 1
#         s += i
#     # print(s)
#
#
# ret1 = timeit("test_while_loop()", globals={"test_while_loop": test_while_loop}, number=100)
# ret2 = timeit("test_for_loop()", globals={"test_for_loop": test_for_loop}, number=100)
# print(ret1 / ret2)

#### 在循环体中避免重复的计算
# from timeit import timeit
#
#
# def test1(n):
#     a = [i**2+1 for i in range(n)]
#     b = [i/sum(a) for i in a]
#     return b
#
#
# def test2(n):
#     a = [i**2+1 for i in range(n)]
#     # 现将使用多次的部分单独计算出来
#     sum_a = sum(a)
#     b = [i / sum_a for i in a]
#     return b
#
# # ret1 = test1(100)
# # ret2 = test2(100)
# # print(ret1 == ret2)
#
# ret1 = timeit("test1(n)", globals={"test1": test1, "n": 200}, number=100)
# print(ret1)
# ret2 = timeit("test2(n)", globals={"test2": test2, "n": 200}, number=100)
# print(ret2)
# print(ret1 / ret2)


### 加速函数
#### 用循环机制代替递归函数

# from timeit import timeit
# def ca_fib1():
#     def fib(n):
#         return(1 if n in (1, 2) else fib(n-1) + fib(n-2))
#
#     ret = fib(30)
#     return ret
#
#
# def ca_fib2():
#     # 使用循环代替递归
#     def fib(n):
#         if n in (1, 2):
#             return(1)
#         a, b = 1, 1
#         for i in range(2, n):
#             a, b = b, a + b
#         return(b)
#
#     ret = fib(30)
#     return ret
#
# ret1 = timeit("ca_fib1()", globals={"ca_fib1": ca_fib1}, number=2)
# ret2 = timeit("ca_fib2()", globals={"ca_fib2": ca_fib1}, number=2)
# print(ret1)
# print(ret2)
# print(ret1 / ret2)   # 这个貌似速度差不多的

#### 使用缓存机制加速递归函数

from timeit import timeit
from functools import lru_cache

def ca_fib1():
    def fib(n):
        return(1 if n in (1, 2) else fib(n-1) + fib(n-2))

    # ret = fib(30)
    ret2 = fib(35)
    return


def ca_fib2():
    @lru_cache(100)
    def fib(n):
        return(1 if n in (1, 2) else fib(n-1) + fib(n-2))
    # ret = fib(30)
    ret2 = fib(35)
    return


ret1 = timeit("ca_fib1()", globals={"ca_fib1": ca_fib1}, number=2)
ret2 = timeit("ca_fib2()", globals={"ca_fib2": ca_fib1}, number=2)
print(ret1)
print(ret2)
print(ret1 / ret2)


#### 使用 numpy 加速 python 函数


















