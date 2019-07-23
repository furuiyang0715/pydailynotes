# 向量计算的优势： Numpy能够充分的利用并行化
import numpy as np
import time


def log_method_time_usage(func):
    def wrapped(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        dt = time.time()-start
        print(f"[TimeUsage] {func.__module__}.{func.__name__} usage: {dt}")
        return result
    return wrapped


a = np.random.rand(100000)
b = np.random.rand(100000)


@log_method_time_usage
def use_for():
    """使用 for 循环"""
    c = 0
    for i in range(100000):
        c += a[i]*b[i]
    return c


@log_method_time_usage
def use_np():
    """使用向量化处理"""
    c = np.dot(a, b)
    return c


if __name__ == "__main__":
    print(use_for())
    print()
    print()
    print(use_np())
