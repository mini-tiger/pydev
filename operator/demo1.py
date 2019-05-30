# coding:utf-8
import operator

a = [2, 'abc', 3]
b = operator.itemgetter(1)  # 定义函数b，获取对象的第1个域的值
print(b(a))

b = operator.itemgetter(1, 0)  # 定义函数b，获取对象的第1个域和第0个域的值
print(b(a))

ss = ["0111", "022", "334", "00"]
print(sorted(ss, key=operator.itemgetter(1)))  # 按照第二个域排序
