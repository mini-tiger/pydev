class A(object):
    def run(self):
        print("this is className %s" % self.__class__.__name__)


class B(object):
    def run(self):
        print("this is className %s" % self.__class__.__name__)


class AA(A):
    def run(self):
        print("this is father className %s" % A.__class__.__name__)
        print("this is className %s" % self.__class__.__name__)

'''·
Ex 函数接受的参数，只要传入的类 有run方法都可以，
'''
def Ex(cls):
    cls.run()

if __name__ == "__main__":
    # a = A()
    Ex(A())
    Ex(AA())
    Ex(B())
