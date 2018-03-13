# coding:utf-8


def jisuan(n, num):
    if n <= 0:
        print '除尽用了{}次'.format(num)
        global a
        a = num
        return num  # 不能返回num,只能赋值全局变量

    n = n // 2
    num += 1
    print num
    jisuan(n, num)

jisuan(100, 0)
print a

print '**'*50

def generator_ex(n,num=0):
	while True:
	    if n <= 0:
	    	print '除尽用了{}次'.format(num)
	        raise StopIteration
	    n = n // 2
	    num+=1
	    yield num

g=generator_ex(100)
for i in g:
	print i