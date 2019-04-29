
# 单实例查看baseic

# 构建类的用法
class A:
    def __init__(self, *args):
        print('I am in A')
        print("this is a args", args)
    def aa(self):
        print('I am in A func aa')


class B:
    def __init__(self, name):
        self.name = name


class C:
    def __init__(self, name):
        self.name = name


class ABC:
    def __new__(cls, *args, **kwargs):
        if args[0] == 'A':
            ins = A.__new__(A, *args, **kwargs)
            ins.__init__(*args, **kwargs) # todo 需要手动调用 init方法
            return ins
        elif args[0] == 'B':
            return B.__new__(B, *args, **kwargs)
        else:
            return C.__new__(C, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        print('I am in ABC')
        print(args)


a = ABC('A')
print(a.__class__)
print("aa" in a.__dir__())
a.aa()
'''
I am in A
this is a args ('A',)
<class '__main__.A'>
True
I am in A func aa
'''
