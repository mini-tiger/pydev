import pandas

food_info = pandas.read_csv("food_info.csv")
print(type(food_info))
# print(help(food_info))
# print(food_info.dtypes) # 包含的所有的变量类型，字符串为object

first_rows = food_info.head()
print(first_rows)
# print(food_info.head(3)) # 可以设置打印前几行，默认5行
print(food_info.tail(3))  # 可以设置打印后几行，默认5行
print(food_info.columns)  # 列名
print(food_info.shape)  # （行数，列数）
