import numpy

import numpy as np
# todo http://www.voidcn.com/article/p-nrrdwtmy-cm.html
# todo https://blog.csdn.net/u010199356/article/details/85697860
# #int8，int16，int32，int64 可替换为等价的字符串 'i1'，'i2'，'i4'，以及其他。

# 数据类型https://wizardforcel.gitbooks.io/ts-numpy-tut/content/3.html
# todo 类似于对象 字典 方式 创建
student = np.dtype([('name', 'S20'), ('age', 'i1'), ('marks', 'f4')])

a = np.array([('abc', 21, 50), ('xyz', 18, 75)], dtype=student)
print(a)
print(type(a))
print(a["name"])
# [(b'abc', 21, 50.) (b'xyz', 18, 75.)]
# <class 'numpy.ndarray'>
# [b'abc' b'xyz']

print("*" * 100)
x = np.empty(shape=[3, 2], dtype=int, order="C")
# 数组 3 行两列，整形， 行优先 创建 随机值 数组
print(x)

# x = np.empty(shape=[3,2], dtype = int,order="F")
# # 数组 3 行两列，整形， 列优先 创建 随机值 数组
# print (x)

# todo 创建默认 元素为0的数组
# 默认为浮点数
x = np.zeros(5)
print(x)
# 设置类型为整数
y = np.zeros((5,), dtype=np.int)
print(y)
# 自定义类型
z = np.zeros((2, 2), dtype=[('x', 'i4'), ('y', 'i4')])
print(z)

# todo 创建默认 元素为1的数组
# 默认为浮点数
x = np.ones(5)
print(x)

# 自定义类型
x = np.ones([2, 2], dtype=int)
print(x)

# 通过 列表，元组 创建
x = [(1, 2, 3), (4, 5)]
a = np.asarray(x)
print(a)
x = (1, 2, 3)
print(np.asanyarray(x, dtype=float))

# 生成range
import numpy as np

x = np.arange(10, 20, 2, dtype=float)
print(x)

# todo 等差数组, 等比数组（numpy.logspace 忽略）
a = np.linspace(start=10, stop=20, num=5, endpoint=False, retstep=True, dtype=int)
# 生成等差 10-20 之间 的5个数，endpoint 是否包括20，restep 是否显示差值
print(a)  # (array([10, 12, 14, 16, 18]), 2.0)

# todo 随机生成
# 生成两行3列 矩阵
print(np.random.random((2, 3)))


data = np.sin(np.arange(20)).reshape(5,4)
print(data) # 生成 5行4列
ind = data.argmax(axis=0) # 按照列 生成 最大值的索引
print(ind)
data_max = data[ind, range(data.shape[1])] # data数组 按照索引 生成range(data.shape[1]=4)

print(data_max)


# 重复使用一个数组，生成矩阵
a = np.arange(0, 40, 10)
b = np.tile(a, (2, 2))
print(b)
# [[ 0 10 20 30  0 10 20 30]
#  [ 0 10 20 30  0 10 20 30]]

#todo 对角矩阵
print(numpy.eye(5,5))
# [[1. 0. 0. 0. 0.]
#  [0. 1. 0. 0. 0.]
#  [0. 0. 1. 0. 0.]
#  [0. 0. 0. 1. 0.]
#  [0. 0. 0. 0. 1.]]