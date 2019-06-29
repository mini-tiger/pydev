import numpy as np

# 交换矩阵的其中两行
a = np.arange(10).reshape(2, 5)
print(a)
a[[0, 1]] = a[[1, 0]]
print(a)

# 找出数组中与给定值最接近的数
z = np.array([[0, 1, 2, 3], [4, 5, 6, 7]])
a = 5.1
print(np.abs(z - a).argmin())

# 判断二维矩阵中有没有一整列数为0？
z = np.random.randint(0, 3, (2, 10))
print(z)
print(z.any(axis=0))

import numpy as np

# 1:8*8棋盘矩阵，其中1、3、5、7行&&0、2、4、6列的元素置为1   1 ,3，5，7列&&0,2,4,6行也是1
z = np.zeros((8, 8), dtype=int)
z[1::2, ::2] = 1
z[::2, 1::2] = 1
print(z)

#归一化，将矩阵规格化到0～1，即最小的变成0，最大的变成1，最小与最大之间的等比缩放
z = 10*np.random.random((5,5))
print(z)
zmin,zmax = z.min(),z.max()
z = (z-zmin)/(zmax-zmin)
print(z)
