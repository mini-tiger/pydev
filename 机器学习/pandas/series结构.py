import pandas as pd
from pandas import Series
fandango = pd.read_csv('fandango_score_comparison.csv')
series_film = fandango['FILM'] # series 是自定义数据的集合， 某列
series_rt = fandango['RottenTomatoes']
# print(fandango[0:5]) # 某些行

film_names = series_film.values
#print type(film_names)
# print(film_names)
rt_scores = series_rt.values
#print rt_scores
series_custom = Series(rt_scores , index=film_names) # 使用Series 转换为 索引是file_names, 数值是rt_scores
print(series_custom[0:5])
print("*"*100)
print(series_custom[['Minions (2015)', 'Leviathan (2014)']]) # 使用列索引
print("*"*100)
# 重新排序 电影名
#方法一
original_index = series_custom.index.tolist()
#print original_index
sorted_index = sorted(original_index)
sorted_by_index = series_custom.reindex(sorted_index) # 按照电影名排序
print(sorted_by_index.head())
print("---------------------------")
#方法二
print(series_custom.sort_index().head())
# print(series_custom.sort_values())

print("*"*100)
# todo series 合并
import numpy as np
# Add each value with each other
print(np.add(series_custom[0:5], series_custom[0:5]))
# Apply sine function to each value
# np.sin(series_custom)
# Return the highest value (will return a single value not a Series)
print(np.max(series_custom))

print("*"*100)
# 判断 筛选
# print(series_custom > 50)
series_greater_than_50 = series_custom[series_custom > 50]

criteria_one = series_custom > 50
criteria_two = series_custom < 75
both_criteria = series_custom[criteria_one & criteria_two] # 分类大于 50 并且小于75
print(both_criteria[0:5])

print("*"*100)
#data alignment same index
rt_critics = Series(fandango['RottenTomatoes'].values, index=fandango['FILM'])
rt_users = Series(fandango['RottenTomatoes_User'].values, index=fandango['FILM'])
rt_mean = (rt_critics + rt_users)/2

print(rt_mean[0:5])

