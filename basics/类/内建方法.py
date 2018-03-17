
# coding:utf-8
##new
class cc(object):
    n = 0  #记录被调用次数
    def __new__(self,*a,**k):
        self.a = 0
        print a
        print k
        # print cls.n
        return super(cc, self).__new__(self,*a,**k)

    def __init__(self,*a,**k):
        self.aaa = 1
        cc.n += 1

    def aa(self):
        return 1


print cc().__class__.__name__  
'''
()
{}
cc
'''
print cc().a  
'''
()
{}
0
'''
print cc().aa()  
'''
()
{}
1
'''
print dir(cc)  # [...., 'a', 'aa', 'n']
abc = cc(1,dd=1)
'''
(1,)
{'dd': 1}
'''
abc1 = cc(1,dd=2)
'''
(1,)
{'dd': 2}
'''
print cc.n   ##被调用5次



print '-' * 50
##slots
class cc1(object):
    
    __slots__ = ('aa','bb') ##限制类中 变量的名字

    def __init__(self):
        super(cc1, self).__init__()
        self.aa = 1
        self.bb=2


c=cc1()
print c.aa,c.bb        ##1 2 
print cc1().aa,cc1().bb   ##1 2 

c.aa=1
c.bb=1
try:
    c.ab=2
except AttributeError :
    print '被 __slots__ 限制'

print '-' * 50
##del
class cc2(object):
    

    def __init__(self):
        super(cc2, self).__init__()
        self.aa = 1
        self.bb=2
    def __del__(self):
        print '{}被删除'.format(self.__class__.__name__)

c=cc2()
del c
'''
print '{}被删除'.format(self.__class__.__name__)
cc2被删除
'''
print '-' * 50
##call  getattr setattr
class cc2(object):
    

    def __init__(self):
        # super(cc2, self).__init__()
        self.aa = 1


    def __call__(self,*a,**k): ##拦截 () 号
        print '被调用的类: {}'.format(self.__class__.__name__)     


    def __getattribute__(self,*args, **kwargs):
        # return k
        return object.__getattribute__(self, *args, **kwargs)
        # return None

    def __setattr__(self,k,v):  ##拦截 ＝ 号
        print '变量名: {}, 赋值:{}'.format(k,v)
        self.__dict__[k]=v   



    def __delattr__(self,k):
        print '被删除变量名: {}'.format(k)        
        # super(cc2, self).__delattr__()
        object.__delattr__(self,k)

c=cc2()
c(1,ad=1) 
'''
变量名: aa, 赋值:1   ##这里注意 self.aa=1 调用 了 _setattr__方法
被调用的类: cc2
'''

print dir(c0
1)
c.ad=22
print c.aa
print c.__dict__
'''
变量名: ad, 赋值:22
{'aa': 1, 'ad': 22, 'bb': 2}
'''

del c.ad
'''
被删除变量名: ad
'''

class cc3(object):
    nn=0
    n=0
    def __new__(self):
        self.n=1
        return super(cc3, self).__new__(self)
    @classmethod
    def class_var(cls):
        print cls.nn
        print cls.n  ##

    @staticmethod
    def static_var():
        print 'thisis static_var'


cc=cc3()
cc.class_var() 
'''
0
1 
self.n 覆盖 n=0
'''
cc.static_var() #'thisis static_var'
