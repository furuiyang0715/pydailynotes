# ref: https://stackoverflow.com/questions/42049147/convert-list-to-pandas-dataframe-column

import pandas as pd

ll = list(range(100))

# create a new df
df = pd.DataFrame({"col": ll})
print(df)


# write to csv
# ...
