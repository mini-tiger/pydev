# coding:utf-8


# 继承
class aa(object):

    def __init__(self):
        print 'this is {}'.format(self.__class__.__name__)
        print 'basic class is {}'.format('aa')


class bb(object):

    def __init__(self):
        print 'this is {}'.format(self.__class__.__name__)
        print 'basic class is {}'.format('bb')


class aabb(aa, bb):
    pass

ab = aabb()  # 从左向右继承
'''
this is aabb
basic class is aa
'''
print '-' * 50


class A(object):  # 定义新式类

    def test(self):
        print self.__class__.__name__
        print('frome A')


class B(A):

    def test(self):
        print('frome B')


class C(A):

    def test(self):
        print('frome C')


class D(B):

    def test(self):
        print('frome D')


class E(C):

    def test(self):
        print('frome E')


class F(D, E):

    def test(self):
        # super(F, object).__init__(self)
        print('frome F')


f1 = F()
# f1.test()
print(F.__mro__)
'''
(<class '__main__.F'>, <class '__main__.D'>, <class '__main__.B'>, <class '__main__.E'>, <class '__main__.C'>, <class '__main__.A'>, <type 'object'>)
'''
# 顺序
'''
D -> B -> A
E -> C -> A
'''
