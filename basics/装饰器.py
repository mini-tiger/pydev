# coding:utf-8

# 装饰器

from functools import wraps

def w(func):
    @wraps(func)
    def bibao(*args,**kw):
        if kw:
            ret = func(*args,**kw)
            return ret
        else:
            return func(a=2)
    return bibao

@w
def aaa(a):
    return a

print aaa(a=1)
print aaa()
# 不加上面的 @wraps(func),会打印bibao
print aaa.__name__



def wrapp(a):
    def bibao1(func):
        def bibao(n):
            print '%d %5d %s' % (a, func(n), 3)
        return bibao
    return bibao1


@wrapp(a=1)
def func1(n):
    return n

f1 = func1(2)  # 1 2 3


###
def wrapp1(func):
    def bibao():
        print func()
    return bibao


@wrapp1
def func2():
    return 1

func2()


##
def wrapp2(var):
    def bibao(func):
        def bibao1(a, b):
                # print x,y
            if var > 10:
                a = 1
                b = 2
                return func(a, b)
            else:
                a = 2
                b = 3
                return func(a, b)
        return bibao1
    return bibao


@wrapp2(10)
def func3(x, y):
    print x + y

func3(2, 3)


##
def wrapp3(cls):
    def bibao(*a):
        a=cls(*a)
        return a.test()
    return bibao



@wrapp3
class cls(object):

	def __init__(self, *a):
		# super(cls, self).__init__()
		self.a=a

	def test(self):
		print self.a


c=cls(1)