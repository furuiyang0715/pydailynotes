# 与时间相关均线的计算

# 查看相关的 csv 文件

# 首先我拿到的一个原始的示例是 xlsx 格式的
# 先转换为 csv 格式，方便后续读取数据进行处理
# Python xlsx 和 csv 之间的相互转换: https://blog.csdn.net/qq_33689414/article/details/78307031

import xlrd   # 安装 pip install xlrd
import csv
import codecs


def xlsx_to_csv():
    workbook = xlrd.open_workbook('zzz.xlsx')
    table = workbook.sheet_by_index(0)
    with codecs.open('ret.csv', 'w', encoding='utf-8') as f:
        write = csv.writer(f)
        for row_num in range(table.nrows):
            row_value = table.row_values(row_num)
            write.writerow(row_value)


# if __name__ == '__main__':
#     xlsx_to_csv()

# 这时就有了一个可以使用 pandas 读取的 csv 文件：ret.csv
# 使用 pd 读出 last 收盘价这一列的数据

import pandas as pd
import functools
import operator

data = pd.read_csv("ret.csv")
# print(data)

# 读取 last 这一列的数据 转换为列表的形式
last = data['Last'].tolist()
# print(last)
print(len(last))
# print(type(last))

# 假如说是以前 3 天的数据作为初始值，首先就应该先计算前 3 天的和
h3 = functools.reduce(operator.add, last[:3]) / len(last[:3])
# print(h3)

# 组成新的临时列表
temp = [h3] + last[3:]
# print(temp)

#
# 出现 bug 这样打包不对 会使数据缺少 因为一个数据打包了一次
print(temp)
print(len(temp))

print(iter(temp))
print(*iter(temp))
# print( type(  *iter(temp)  ))


# ret = zip(*[iter(temp)]*2)
# print(ret)


# # 解包 计算新列
# def gen_H():
#     for (x, y) in ret:
#         # print(x, y)
#         yield x+y
#
# new_list = list(gen_H())
#
# # 将新列进行处理
# new_list = new_list + [0, 0]
# print(new_list)
# print(len(new_list))



