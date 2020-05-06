# coding:utf-8

# 装饰器

from functools import wraps
import time

def mydec(func):
    @wraps(func)
    def mywrap(*args, **kw):
        print('hello this is decorator1')
        func(*args, **kw)
    return mywrap

@mydec
def hello_world():
    pass

# xxx 等价于执行mydec(hello_world)()
cur = mydec(hello_world)
cur()


print("===" * 50)


def mydec1(type_=None):
    def decorate(func):
        @wraps(func)
        def mywrap():
            if type_ is not None:
                print(type_)
            func()
        return mywrap
    return decorate

@mydec1(type_='test2')
def helloWorld():
    print('hello, world')


# xxx 等价于执行下面
cur1 = mydec1('test1')
cur2 = cur1(helloWorld)
cur2()



