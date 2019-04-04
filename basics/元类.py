# 类也是对象

# todo 默认方式创建类
class A(object):
    aa = 1


# 类的属性
print(A.__class__, A.__dict__)
# <class 'type'> {'__module__': '__main__', 'aa': 1, '__dict__': <attribute '__dict__' of 'A' objects>, '__weakref__': <attribute '__weakref__' of 'A' objects>, '__doc__': None}


# todo 通过type 创建
# type(类名, 父类的元组（针对继承的情况，可以为空），包含属性的字典（名称和值）)
A1 = type('AA', (), {'aa': 1})  # todo 这里的类名是 AA,变量名不是A1
A2 = type('AAA', (A,), {'bb': 2})  # todo 这里的类名是 AA,变量名不是A1

# A1是类对象 ，没有实例化
print(A1.__class__, A1.__dict__)
# <class 'type'> {'aa': 1, '__module__': '__main__', '__dict__': <attribute '__dict__' of 'AA' objects>, '__weakref__': <attribute '__weakref__' of 'AA' objects>, '__doc__': None}
print(A2.__class__, "父类:", A2.__bases__, "属性:", A2.__dict__)

a1 = A1()
setattr(a1, "a", 1)
print(a1.__class__, a1.__dict__)
# <class '__main__.AA'> {'a': 1}


# todo    type实际上是一个元类。type就是Python在背后用来创建所有类的元类
tmpInt = int(1)
tmpStr = "1"  # str(1)
tmpList = [1, 2, 3]
print("内置int类:", int.__class__, "tmpInt的类的类(元类):", int.__class__.__class__)
print("tmpInt的类:", tmpInt.__class__, "tmpInt的类的类(元类):", tmpInt.__class__.__class__)
print("tmpStr的类:", tmpStr.__class__, "tmpStr的类的类(元类):", tmpStr.__class__.__class__)
print("tmpList的类:", tmpList.__class__, "tmpList的类的类(元类):", tmpList.__class__.__class__)

# 通过type 动态创建类
print("=" * 20, "通过type 动态创建类", "=" * 20)
for i in range(2):
    tmpC = type('AA', (), {'aa': i})  # todo 这里的类名是 AA,变量名不是A1
    print(tmpC.__class__, tmpC.__dict__)

print("=" * 20, "通过type 组合不同函数创建类", "=" * 20)


def __init__(self):
    self.message = 'Hello World'


def say_hello(self):
    print(self.message)


attrs = {'__init__': __init__, 'say_hello': say_hello}
bases = (object,)
Hello = type('Hello', bases, attrs)

h = Hello()
h.say_hello()

print("=" * 20, "通过metaclass创建类", "=" * 20)


# todo  创建类 metaclass
# metaclass是创建类，所以必须从`type`类型派生：
class Meta(type):
#     __new__()方法接收到的参数依次是：
# 当前准备创建的类的对象 ；
# 类的名字 name；
# 类继承的父类集合 bases；
# 类的方法集合 namespace
    def __new__(cls, name, bases, namespace, **kwargs):
        print("当前类名:", name, "当前类的父类:", bases, "方法集合:", namespace)
        print("kwargs:",kwargs)
        # todo 如果派生的子类 没有bar方法或者attrA属性，报错
        if  ('bar' not in namespace) or ('attrA' not in namespace):
            raise TypeError('bad user class')
        return super().__new__(cls, name, bases, namespace, **kwargs)


class Base(object, metaclass=Meta):
    attrA=1
    def bar(self):
        return "this is Base"

try:
    class Base1(object, metaclass=Meta):
        attrA=2 # 没有 bar 方法
except TypeError as te:
    print("this is typeErr:",te)

