import numpy

world_alcohol = numpy.genfromtxt("world_alcohol.txt", delimiter=",", dtype=str, skip_header=1)
print(type(world_alcohol))
print(world_alcohol[0, -1])  # 第0行，最后一列，等于[0,4]
# print(world_alcohol)
# print(help(world_alcohol))

l1 = list(map(lambda x: 5 * x, range(0, 4)))
vector = numpy.array(l1)
matrix = numpy.array([[5, 10, 15], [20, 25, 30], [35, 40, 45]])
matrix2 = numpy.array([
	[[5, 10, 15], [20, 25, 30], [35, 40, 45]],
	[[55, 60, 65], [70, 75, 80], [85, 90, 95]
	 ]
])
# print(vector)
print(vector.shape)  # (4,)，一维数据 vector 4列，每个是一个数字
print(vector[2])  # 取第二个索引值
# print(matrix)
print(matrix.shape)  # (3, 3) ，二维数据 matrix 有3行，每行下的一维有3列
print("所有一维行 ，0:2是 第0与1索引位置的值", matrix[:, 0:2])  # 所有一维行 第2索引位置的值
# print(matrix2)
print(matrix2.shape)  # (2,3, 3) ，三维数据 matrix 有2行，每个二维数组有3列，每个二维下的一维有3列
print("所有二维行 第1索引位置的值", matrix2[:, 1])

# 保证元素数据类型一样
nums = numpy.array([1, 2, 3, 4.0, "5"])
print(nums)
print(nums.dtype)
