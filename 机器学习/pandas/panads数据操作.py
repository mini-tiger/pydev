import pandas as pd
from pandas import Series
fandango = pd.read_csv('fandango_score_comparison.csv')

print(type(fandango))
fandango_films = fandango.set_index('FILM', drop=False) # FILM 列，设置为索引列
print(fandango_films["Avengers: Age of Ultron (2015)":"Hot Tub Time Machine 2 (2015)"]) # 类似列表切片
print(fandango_films.loc["Avengers: Age of Ultron (2015)":"Hot Tub Time Machine 2 (2015)"]) # 类似列表切片索引
# print(fandango_films[0:5]) # 使用索引数值 可以继续使用

movies = ['Kumiko, The Treasure Hunter (2015)', 'Do You Believe? (2015)', 'Ant-Man (2015)'] # 单独取
print(fandango_films.loc[movies])


print("*"*100)

import numpy as np

# returns the data types as a Series
types = fandango_films.dtypes
# print(types)
# FILM                           object
# RottenTomatoes                  int64
# RottenTomatoes_User             int64
# Metacritic                      int64
# Metacritic_User               float64 ....
# filter data types to just floats, index attributes returns just column names
float_columns = types[types.values == 'float64'].index # 列 是float64类型的列名
# print(float_columns)
# use bracket notation to filter columns to just float columns
float_df = fandango_films[float_columns]
# print(float_df)
# `x` is a Series object representing a column
deviations = float_df.apply(lambda x: np.std(x)) # 标准差

print(deviations)