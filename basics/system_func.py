# coding:utf-8
from __future__ import print_function
import env
from set_list_dict_tuple import print_ex

# import sys
# print(dir(sys.modules['__builtin__']))
l1=env.list_ex(4)
print (l1)
print_ex('sorted list排序 :', sorted(l1,reverse=True))
d1=env.dict_ex(4)
print (d1)
print_ex('sorted dict排序 :', sorted(d1.items(),key=lambda x:x[0],reverse=False))

s = 'ab0s'
l = [1, 2, 0, 3]
print(s.split('a'), all(s.split('a')))
print(l, all(l))
print(xrange(1, 3), all(xrange(1, 3)))
print(l)
print_ex('all() 可迭代对象,只要有一个0或false， 返回False :', 'all(l)')
print(all(l))
print_ex('any() 可迭代对象,全为0或false， 返回False :', 'any(l)')
print(any(l))


print_ex('enumerate() 返回可迭代对象的 下标和值，第二参数为 从哪个下标开始 :',
         'enumerate(xrange(10, 2))')
for i, v in enumerate(xrange(10), 2):
    print(i, v)

print ("{:#^100}".format('''转换 码'''))
print('返回字符对应的 ASCII 数值，或者 Unicode 数值 :', 'ord(a)')
print(ord('a'))

print('返回数对应的 ASCII 数值 :', 'chr(97)')
print(chr(97))

print('返回数对应的 unicode 的字符 :', 'unichr(7)')
print(unichr(97))

print('返回对象的字符串格式 :', 'str(env.dict_ex(3))')
print(str(env.dict_ex(3)))


print('bin(2) 转换为二进制 :', bin(2))

print ("{:#^100}".format('''计算'''))

print_ex('abs 绝对值', abs(-112233.1))

print_ex('divmod返回地板除和余数的元组(a // b, a % b) :', divmod(7, 2))

import math   # 导入 math 模块

print("计算x的y次方 math.pow(100, 2) : ", math.pow(100, 2))
# 使用内置，查看输出结果区别
print("pow(100, 2) : ", pow(100, 2))

print("math.pow(100, -2) : ", math.pow(100, -2))
print("math.pow(2, 4) : ", math.pow(2, 4))
print("math.pow(3, 0) : ", math.pow(3, 0))

print("sum([1,2],start=) strart是从哪个数开始加: ", sum([1, 2], 2))

print("round(7.056,3) 四舍五入保留3位小数 : ", round(7.056,2))

print ("{:#^100}".format('''判断类型'''))

print("isinstance(1,int)判断一个对象是否是一个已知的类型: ", isinstance(1, int))
print("type(1)对象是类型: ",  type(1) == int)


class A:
    pass


class B(A):
    pass


print('for i in iter("12"):	print (i)', "返回可迭代对象")
for i in iter('12'):
    print(i)


print('bool 返回真假', bool(chr(97) == 'a'))    # 返回 True


print('map(lambda x,y:pow(x,y),xrange(4),xrange(4)) 提供序列，依次执行函数，返回新序列',
      map(lambda x, y: pow(x, y), xrange(4), xrange(4)))

print('filter(lambda x,y:pow(x,y),xrange(4),xrange(4)) 提供序列，依次执行函数，返回新序列',
      filter(lambda x: x>1, xrange(4)))

