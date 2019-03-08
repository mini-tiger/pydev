# -*- coding: utf-8 -*-
import platform
import sys

print(sys.version)
print(sys.version_info)
print(platform.python_version())


def print_func(str):
	print("=" * 20 + str + "=" * 20)


# 三元运算，三目运算
print_func("三元运算，三目运算")
a = 2
b = 3
print("true") if a > b else print("false")
min = a if a < b else b
print(min)

print_func("args,kwargs")

def ak(first, *args, **kwargs): # 其它形参写在 args前面
	print(first) # 1
	print(args) # (2, [3, 4])
	print(*args) # 2 [3, 4]
	print(kwargs) # {'a': 1, 'b': 2}

ak(1, 2, [3, 4], a=1, b=2)

print_func("负索引")
a=list(map(lambda x:x+1,range(10)))
print(a)
print(a[::-1]) # [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
b=sorted(a,reverse=True)
print(b)