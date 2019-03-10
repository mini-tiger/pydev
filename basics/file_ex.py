# coding:utf-8

import env
from env import func
print(func.Func1())
print(func.Obj1().c())

s=env.str_ex(8)
l=env.list_ex(8)
print 's: {}'.format(s)
print 'l: {}'.format(l)
f=open('1.txt',mode='w+')
f.write(s)
f.write('\n')
f.writelines(l)
f.write('\n')
# f.flush() #手动 写到硬盘上
f.close() #自动也会关闭



with open('1.txt',mode='a+') as f:
	l1=env.list_ex(10)
	print 'l1: {}'.format(l1)
	f.seek(0, 0) # 不起作用
	f.writelines(l1)
	f.write('\n')



with open('1.txt',mode='r+') as f:
	print '位置从0到1 的是 ： {}'.format(f.read(1))
	print '位置从1到3 的是 ： {}'.format(f.read(2))
	
	f.seek(0, 0)  ##重新把指针 放到 开头
	'''
offset -- 开始的偏移量，也就是代表需要移动偏移的字节数
whence：可选，默认值为 0。
给offset参数一个定义，表示要从哪个位置开始偏移；
0代表从文件开头开始算起，
1代表从当前位置开始算起，
2代表从文件末尾算起。
	'''
	print '位置从0到1 的是 ： {}'.format(f.read(1))
	f.seek(0, 0)  ##重新把指针 放到 开头
	# readline(1) 读出指定个字节,默认为一行
	print (f.readline(1),f.readline(),f.readline())

	f.seek(-10, 2) #从结尾 往前 读 10个字符
	print f.readlines() ##列表

	print '获得文件指针 : {}'.format(f.tell()) 


