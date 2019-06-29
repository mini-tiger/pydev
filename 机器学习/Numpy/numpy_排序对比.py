import numpy as np

data = np.sin(np.arange(20)).reshape(5, 4)
print(data)  # 生成 5行4列
ind = data.argmax(axis=0)  # 按照列 生成 最大值的索引
print(ind)
data_max = data[ind, range(data.shape[1])]
print(data_max)
print(all(data_max == data.max(axis=0)))  # True, data数组 按照索引 生成range(data.shape[1]=4)

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
print(j) # 从小到大的 索引值
print(a[j]) # 按照索引显示
