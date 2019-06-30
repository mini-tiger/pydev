import numpy as np

# todo 最大值，最小值， 中位数(中间大小的值), 最大最小值的差，平均值，加权平均值，可以按照轴
#加权平均值
a = np.array([1, 2, 3, 4])
print('我们的数组是：')
print(a)
print('调用 average() 函数：')
print(np.average(a))

# 不指定权重时相当于 mean 函数
wts = np.array([4, 3, 2, 1])
print('再次调用 average() 函数：')
print(np.average(a, weights=wts))
# 如果 returned 参数设为 true，则返回权重的和
print('权重的和：')
print(np.average([1, 2, 3, 4], weights=[4, 3, 2, 1], returned=True))

a = np.array([[3, 7, 5], [8, 4, 3], [2, 4, 9]])
print('我们的数组是：')
print(a)
# [[3 7 5]
#  [8 4 3]
#  [2 4 9]]
print('调用 amin() 函数：')
# 每行最小值
print(np.amin(a, axis=1))  # 按照X轴最小值  [3 3 2]

# 第列最小值
print('再次调用 amin() 函数：')
print(np.amin(a, axis=0))  # 按照Y轴最小值 [2 4 3]

print('调用 amax() 函数：')
print(np.amax(a))  # 9

print('再次调用 amax() 函数：')
print(np.amax(a, axis=0))
