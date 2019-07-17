# 在实际的开发中 但我们需要定义常量时，其中的一个办法是用大写变量通过整数来定义
JAN = 1
FEB = 2
MAR = 3
NOV = 11
DEC = 12

# 当然这样做简单快捷，缺点是类型是 int ，并且仍然是变量

# 这时候我们定义一个 class 类型，每个常量都是 class 里面唯一的实例。正好 Python 提供了 Enum 类来实现这个功能

from enum import Enum
Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

# 遍历枚举类型
for name, member in Month.__members__.items():
    print(name, '---------', member, '----------', member.value)


# 第一个参数 Month 表示的是该枚举类的类名，第二个 tuple 参数，表示的是枚举类的值；
# 当然，枚举类通过 __members__ 遍历它的所有成员的方法。
# 注意的一点是 ， member.value 是自动赋给成员的 int类型的常量，默认是从 1 开始的。
# 而且 Enum 的成员均为单例（Singleton），并且不可实例化，不可更改
