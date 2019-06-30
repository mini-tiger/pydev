import pandas

food_info = pandas.read_csv("food_info.csv")

food_info.sort_values("Sodium_(mg)", inplace=True)
# ​ inplace = True：不创建新的对象，直接对原始对象进行修改；
# ​ inplace = False：对数据进行修改，创建并返回新的对象承载其修改结果。

print(food_info["Sodium_(mg)"].head(2))
#Sorts by descending order, rather than ascending.
food_info.sort_values("Sodium_(mg)", inplace=True, ascending=False) # aecending 升序为假，则是降序,默认是升序
print(food_info["Sodium_(mg)"].head(2))

print(food_info["Sodium_(mg)"].tail(2))
# 8251   NaN          NaN 是空值，默认是最小，比0小
# 8267   NaN
# Name: Sodium_(mg), dtype: float64