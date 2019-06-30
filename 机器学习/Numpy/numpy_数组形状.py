import numpy as np

a = np.arange(8)
print('原始数组：')
print(a)

b = a.reshape(4, 2)
print('修改后的数组：')
print(b)
# [[0 1]
#  [2 3]
#  [4 5]
#  [6 7]]

# todo 展开数组
a = np.arange(8).reshape(2, 4)

print('原数组：')
print(a)
# 默认按行

print('展开的数组：')
print(a.flatten())

print('以 F列 风格顺序展开的数组：')
print(a.flatten(order='F'))

print('以 F列 风格顺序展开的数组：ravel会影响原数组')
print(a.ravel(order='F'))

# todo 对换行列数组
# 方法一
a = np.arange(12).reshape(3, 4)
print('原数组：')
print(a)

print('对换数组：')
print(a.T)  # 快捷 变为 3列 4行
print("*" * 100)

# 方法二
# 创建了三维的 ndarray
a = np.arange(8).reshape(2, 2, 2)

print('原数组：')
print(a)
print('\n')
# 现在交换轴 0（深度方向）到轴 2（宽度方向）

print('调用 swapaxes 函数后的数组：')
print(np.swapaxes(a, 2, 0))  # 则是 索引位置0，1，2 交换为 2，1，0 则是 0,2的位置交换
'''
原位置 0，1，1 是3  ，交换0和2的索引位置后 为 1，1，0是3 
'''

# 方法三
a = np.arange(12).reshape(3, 4)

print('原数组：')
print(a)

print('对换数组：')
print(np.transpose(a))  # 不加参数，默认行列对换

print("*" * 100)
print('原数组：')
a = np.arange(16).reshape(2, 2, 4)
print(a)
# [[[ 0  1  2  3]
#   [ 4  5  6  7]]
#
#  [[ 8  9 10 11]
#   [12 13 14 15]]]

print('对换数组：')
# [[[ 0  1  2  3]
#   [ 8  9 10 11]]
#
#  [[ 4  5  6  7]
#   [12 13 14 15]]]
print(np.transpose(a, (1, 0, 2)))
# todo transponse(1,0,2) 对应 原数组索引位置 交换
# todo 原数组位置(0,1,0) 转换为 (1，0，0) 就是 索引（0，1，2）转换为 （1,0,2）
'''
原数组是三维数组(0,1,2) 索引，  改变为 (1,0,2) , 也就是前两位 索引交换位置
例如 原数组 (0,1,0) 位置是4 
索引位置 0对应0，
		1对应1，
		2对应0
		
交换索引位置 为（1，0，2） 则是  （1,0,0)的位置是4
索引位置 0对应1，
		1对应0，
		2对应0		
'''

print("*" * 100)
a = np.floor(10 * np.random.random((3, 4)))
# print a

# a.shape
## flatten the array
# a.ravel()
# a.shape = (6, 2)
# print a
# print a.T
a.resize((2, 6))  # 3行4列，变为 2行6列
print(a)

# If a dimension is given as -1 in a reshaping operation, the other dimensions are automatically calculated:
# a.reshape(3,-1)

# 交换矩阵的其中两行
a = np.arange(10).reshape(2, 5)
print(a)
a[[0, 1]] = a[[1, 0]]
print(a)