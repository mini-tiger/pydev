import numpy as np

# https://www.runoob.com/numpy/numpy-sort-search.html

data = np.sin(np.arange(20)).reshape(5, 4)
print(data)  # 生成 5行4列
ind = data.argmax(axis=0)  # 按照列 生成 最大值的索引
print(ind)
data_max = data[ind, range(data.shape[1])]  # 按照索引  data.shape[1]是4，按照列提取 数据
print(data_max)
print(all(data_max == data.max(axis=0)))  # True,

# 排序
a = np.array([
    [4, 3, 5],
    [1, 2, 1]])
# print a
b = np.sort(a, axis=1)
print(b)
# [[3 4 5]
#  [1 1 2]]

# a.sort(axis=1)
# print(a)

a = np.array([4, 3, 1, 2])
j = np.argsort(a)
print(j)  # 从小到大的 索引值
print(a[j])  # 按照索引显示

arr = np.array([
    [10, 20, 3],
    [4, 58, 6],
    [78, 8, 9]])
print(np.sort(arr, axis=1))  # 按照X轴，行排序
# [[ 3 10 20]
#  [ 4  6 58]
#  [ 8  9 78]]
print("*"*100)

