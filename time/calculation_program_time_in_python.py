# 转载链接： https://mp.weixin.qq.com/s/ml7W3GVeG84gQ8i2TguOuQ
# (1) 测试代码运行时间
import time
tic = time.time()
much_job = [x**2 for x in range(1, 10**6, 3)]
toc = time.time()
print(f"used {toc-tic} s")

# (2) 测试代码多次运行的平均时间
from timeit import timeit
g = lambda x: x**2+1


def main():
    return(g(2)**120)

# 计算 10 次运行的平均时间
ret = timeit("main()", globals={"main":main}, number=10)
print(ret)

# 按照调用函数分析代码运行的时间
import profile

def relu(x):
    return(x if x>0 else 0)


def main():
    res = [relu(x) for x in range(-100000, 100000, 1)]
    return res

profile.run("main()")


# 按行分析代码运行时间
# 安装： pip install --upgrade pip; pip install line_profile
# 或者尝试 sudo pip install --pre line_profiler 或 sudo pip install line_profiler==1.0b3
# 或者尝试使用科学计算环境

from line_profile import LineProfile

def relu(x):
    return(x if x>0 else 0)


def main():
    res = [relu(x) for x in range(-100000, 100000, 1)]
    return res

lprofile = LineProfile(main, relu)
lprofile.run("main()")
lprofile.print_status()