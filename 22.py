

def wrapp(*args):
    def bibao1(func):
        def bibao(a):
            print args
            print func(a)
        return bibao
    return bibao1

@wrapp(11)
def abc(*a):
    return a


abc(1)

l = list(xrange(10))
print l
print map(lambda x: x+1,l)

print filter(lambda x: x>4, l)

class abcd(object):
    def __init__(self):
        pass
    def __call__(self,*args):
        return args

    def __setattr__(self,k,v):
        self.__dict__[k]=v

a = abcd()
print a(11)
a.b=1
a.c=2
print a.c

def gen(n):
    while n>0:
        yield n
        n = n -1
    return

for i in gen(10):
    print i