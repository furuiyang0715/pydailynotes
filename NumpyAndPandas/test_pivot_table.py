import pandas as pd
import numpy as np

data = {'year': ['2016', '2016', '2015', '2014', '2013'],
        'country': ['uk', 'usa', 'fr', 'fr', 'uk'],
        'sales': [10, 21, 20, 10, 12],
        'rep': ['john', 'john', 'claire', 'kyle', 'kyle']
        }
df = pd.DataFrame(data)
print(df)
"""
   year country  sales     rep
0  2016      uk     10    john
1  2016     usa     21    john
2  2015      fr     20  claire
3  2014      fr     10    kyle
4  2013      uk     12    kyle
"""

# df1 = df.pivot_table(index='country', columns='year', values=['rep'])
# print(df1)
"""
pandas.core.base.DataError: No numeric types to aggregate
"""
df2 = df.set_index(['year', 'country']).unstack('year')
# print(df2)


df3 = df.pivot_table(index='country', columns='year', values=['rep', 'sales'], aggfunc='first')
print(df3)
