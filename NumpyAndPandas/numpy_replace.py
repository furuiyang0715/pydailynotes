# numpy 数据的并行替换

import numpy as np

import pandas as pd


# convert a list of dictionaries to numpy matrix

d = [{"a": 1, "b": 4}, {"b": 2}]

res = pd.DataFrame(d).values


print(res)


print(type(res))
