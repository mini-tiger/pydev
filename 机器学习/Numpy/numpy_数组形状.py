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
print (a.ravel(order = 'F'))


# todo 对换行列数组
a = np.arange(12).reshape(3, 4)

print('原数组：')
print(a)

print('对换数组：')
print(np.transpose(a))


a = np.floor(10*np.random.random((3,4)))
#print a

#a.shape
## flatten the array
# a.ravel()
#a.shape = (6, 2)
#print a
#print a.T
a.resize((2,6)) # 3行4列，变为 2行6列
print(a)

#If a dimension is given as -1 in a reshaping operation, the other dimensions are automatically calculated:
#a.reshape(3,-1)