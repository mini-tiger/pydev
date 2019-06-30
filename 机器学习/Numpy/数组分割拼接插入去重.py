# https://www.runoob.com/numpy/numpy-array-manipulation.html
import numpy as np

a = np.floor(10 * np.random.random((2, 2)))
b = np.floor(10 * np.random.random((2, 2)))
print(a)

print(b)

print(np.hstack((a, b)))  # 按行拼接
# [[3. 3.]
#  [2. 8.]]
# [[9. 1.]
#  [2. 0.]]
# [[3. 3. 9. 1.]
#  [2. 8. 2. 0.]]

print(np.vstack((a, b)))  # 按行拼接
# [[9. 8.]
#  [5. 0.]]
# [[7. 7.]
#  [2. 2.]]
# [[9. 8.]
#  [5. 0.]
#  [7. 7.]
#  [2. 2.]]


# 分割
a = np.floor(10 * np.random.random((2, 12)))
# print a
print(np.hsplit(a, 3))  # 2行12列 分割 成3个 2行 4列的数组，    12 /3=4
print(np.hsplit(a, (3, 4)))  # 每行，第3 ，4之间分割，也就是 把第3列 单拿 出来
a = np.floor(10 * np.random.random((12, 2)))
# print(a)
print(np.vsplit(a, 3))  # 12行2列 分割 成3个 4行 2列的数组，    12 /3=4
