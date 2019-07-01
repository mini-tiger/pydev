import numpy as np

# https://www.runoob.com/numpy/numpy-sort-search.html

data = np.array(np.random.randint(10, size=10))
print(data)  # 生成 5行4列
data1 = np.array(np.random.randint(10, size=10))
print(data1)

# 判断一个是否在另一个内
print("data是否有在data1内", np.in1d(data, data1))
print("data是否有在data1内", data[np.in1d(data, data1)])

# 去重
print("去重", np.unique(data))

# 交集
print("交集", np.intersect1d(data, data1))

# 并集
print("并集", np.union1d(data, data1))

# 差集
print("差集", np.setdiff1d(data, data1))

import pandas as pd

data1 = {
    "a": [1, 2, 3], # 转化为 列，而不是行
    "b": [4, 5, 6],
    "c": [7, 8, 9]
}
data2 = {
    "a": [1, 2, 3],
    "b": [4, 5, 6],
    "c": [7, 8, 9]
}

df1 = pd.DataFrame(data1, index=["a", "b", "c"])
df2 = pd.DataFrame(data2, index=["a", "b", "c"])
print(df1)
#    a  b  c
# a  1  4  7
# b  2  5  8
# c  3  6  9
print(np.add(df1, df2)) # index一样，相加对应位置数值
#    a   b   c
# a  2   8  14
# b  4  10  16
# c  6  12  18
