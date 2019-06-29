import numpy

import numpy as np

# #int8，int16，int32，int64 可替换为等价的字符串 'i1'，'i2'，'i4'，以及其他。

# 数据类型https://wizardforcel.gitbooks.io/ts-numpy-tut/content/3.html
student = np.dtype([('name', 'S20'), ('age', 'i1'), ('marks', 'f4')])

a = np.array([('abc', 21, 50), ('xyz', 18, 75)], dtype=student)
print(a)
print(type(a))
print(a["name"])
# [(b'abc', 21, 50.) (b'xyz', 18, 75.)]
# <class 'numpy.ndarray'>
# [b'abc' b'xyz']


# 类型转换
vector = numpy.array(["1", "2", "3"])
print(vector.dtype) # <U1  Unicode
print(vector)
vector = vector.astype(float) # 都改为float
print(vector.dtype)
print(vector)