import numpy

l1 = list(map(lambda x: 5 * x, range(0, 4)))
vector = numpy.array(l1)
print(vector >= 10)  # 判断矩阵每个元素

matrix = numpy.array([[5, 10, 15], [20, 25, 30], [35, 40, 45]])
et_to_len = (matrix > 10)
print(et_to_len)
print(matrix[et_to_len])  # [15 20 25 30 35 40 45], 将所有符合条件 打印出来，一维形式

eq_to_len = (matrix[:, 1] == 10)  # 每行第1 列 是否有等于10，
print(eq_to_len)
print(matrix[eq_to_len])  # 10,25,40是否 等于10
print(matrix[eq_to_len, :])  # [[ 5 10 15]] 找到等于10 的那行
print("*" * 60)
matrix2 = numpy.array([
	[[5, 10, 15], [20, 25, 30], [35, 40, 45]],
	[[55, 60, 65], [70, 75, 80], [85, 90, 95]
	 ]
])
# print(matrix2[:, 1])
# [[20 25 30]
#  [70 75 80]]
et_to_30 = (matrix2[:, 1, 1] >= 30)
# 所有二维行中，第1索引是二维数组，在第1索引是一维数组[55, 60, 65]
# print(matrix2[et_to_30]) # 符合的那行二维数组
# [[[55 60 65]
#   [70 75 80]
#   [85 90 95]]]
print(matrix2[et_to_30, 0:1])  # 符合的一维数组 [[[55 60 65]]]

# 判断条件  and or
vector = numpy.array([5, 10, 15, 20])
eq_to_5_and_10 = (vector == 5) & (vector == 10)
print(eq_to_5_and_10)

vector = numpy.array([5, 10, 15, 20])
eq_to_5_or_10 = (vector == 5) | (vector == 10)
print(eq_to_5_or_10)

# 判断 找到 并赋值
matrix = numpy.array([
	[5, 10, 15],
	[20, 25, 30],
	[35, 40, 45]
])
second_column_25 = (matrix[:, 1] >= 25)  # 10,25,40 里面大于25的
print(second_column_25)
# matrix[second_column_25] = 10 # 将符合条件中,涉及的行 元素赋值是10
# [[ 5 10 15]
#  [10 10 10]
#  [10 10 10]]
# 等价于 matrix[second_column_25,:] = 10
matrix[second_column_25, 0] = 10  # 符合条件中 数组中的 0索引位置重新赋值
print(matrix)
# [[ 5 10 15]
#  [10 25 30]
#  [10 40 45]]


# 求和
vector = numpy.array([5, 10, 15, 20])
print(vector.sum())

matrix = numpy.array([
	[5, 10, 15],
	[20, 25, 30],
	[35, 40, 45]
])
# 按照X轴 求和
print(matrix.sum(axis=1))  # array([ 30,  75, 120])

# 按照y轴 求和
print(matrix.sum(axis=0))  # array([60, 75, 90])

# 乘法
import numpy as np

A = np.array([[1, 1],
              [0, 1]])
B = np.array([[2, 0],
              [3, 4]])
# print(A)
# print(B)
print(A * B)  # 对应位置乘法
# [[2 0]
#  [0 4]]
# 内积 https://blog.csdn.net/u012149181/article/details/78913416
# 结果0，0 位结果是5 ，是 A(0)=[1,1] B的第0列 （2，3）  1*2+1*3
# 结果0，1 位置是4 ，是 A(0)=[1,1] B的第1列 （0，4）  1*0+1*4
# 结果1，0 位置是3 ，是 A(1)=[0,1] B的第0列 （2，3）  0*2+1*3
print(A.dot(B))  # 等价 np.dot(A, B)
# [[5 4]
#  [3 4]]

# 矩阵减法
a = np.array([20, 30, 40, 50])
b = np.arange(4)  # [0,1,2,3]
# print a
# print b
# b
c = a - b
print(c)  # [20 29 38 47] 按索引位减法
print(b ** 2)  # [0 1 4 9],


B = np.arange(3)
print(B) # [0 1 2]
print(np.exp(B)) # exp是常数 2.718.。  ,  2.718 的0次方，到 2次数
print(np.sqrt(B)) # sprt 是根号

print("*" * 100)
# replace nan value with 0
world_alcohol = numpy.genfromtxt("world_alcohol.txt", delimiter=",", skip_header=1)
# 提取数据 存入变量
# print world_alcohol
is_value_empty = numpy.isnan(world_alcohol[:, 4])  # 判断 第5列（索引4） 的矩阵是否有空
# print(is_value_empty)
world_alcohol[is_value_empty, 4] = '0'  # 将空 赋值为0
alcohol_consumption = world_alcohol[:, 4]  #
alcohol_consumption = alcohol_consumption.astype(float)  # 数据转换为float
total_alcohol = alcohol_consumption.sum()  # 求和
average_alcohol = alcohol_consumption.mean()  # 求平均值
print(total_alcohol)
print(average_alcohol)
