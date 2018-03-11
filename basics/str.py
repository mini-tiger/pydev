# coding:utf-8
from __future__ import print_function
import env
from set_list_dict_tuple import print_ex

str1=env.str_ex(3)
print (str1)
str2='123456'
print (str2)

print_ex('count 统计出现次数', '112233'.count('1'))

print ("{:#^58}".format('''更新，切片'''))

print_ex('+ 连接在一起 :', str1+str2)
print_ex('切片 :', (str1+str2)[-1:0:-1])
print_ex('切片，reverse :', (str1+str2)[::-1])
print_ex('切片,步长 :', (str1+str2)[2:-1:2])
print ('str2[0] 获取索引位置的值，不可变类型 :',str2[0])
print ('sqlit 以 str 为分隔符,第二个参数分隔次数','1112223333'.split('2',1))
print ('sqlitlilnes 按照行\\r, \\r\\n, \\n分隔','111 \n 222 \r 3333'.splitlines())

print ("{:#^58}".format('''格式化'''))
print ('good,bye , capitalize()'.capitalize())
print ('good,bye , title()'.title())
print ('good,bye , lower()'.lower())
print ('good,bye , upper()'.upper())
print ('good,bye , swapcase,翻转大小写()'.swapcase())

print ('ljust(50) 左对齐 参数为占用字符数'.ljust(50))

print ('rjust(50) 右对齐 参数为占用字符数'.rjust(50))
print ('center(50) 居中对齐 参数为占用字符数'.center(50))
print ('zfill(50) 右对齐,左边填充0','20'.zfill(10))
print ('format 方法 忽略')


print ("{:#^58}".format('''查找'''))

print_ex('find,查到是索引值 ，否则-1,rfind从右侧开始 :', str2.find('2'))
print_ex('index,查到是索引值 ，否则报错,rindex从右侧开始 :', str2.index('2'))


print ("{:#^58}".format('''改'''))
print_ex('strip,去除空格 : rstrip从右侧 :', '  dddd   '.strip())
print_ex('replace 替换，第三个参数是替换次数 :', str2.replace('1','2',1))


print ("{:#^58}".format('''判断'''))
print (str1)
print_ex('isdigit 是否整数 :', '123'.isdigit())
print_ex('istitle 是否首字母大写 :', str1.istitle())
print_ex('islower 是否都小写 :', str1.islower())
print_ex('isupper 是否都大写 :', str1.isupper())