# 方法一
class cls10(object):
    def __new__(cls, *a, **w):
        if not hasattr(cls10, '_i'):  # 单实例方式
            cls10._i = super(cls10, cls).__new__(cls, *a, **w)
        return cls10._i

    def __init__(self, *a, **w):
        pass

cc1=cls10()
cc2=cls10()
print(id(cc1) == id(cc2))

# 方法二
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Cls4(metaclass=Singleton):
    pass


cls1 = Cls4()
cls2 = Cls4()
print(id(cls1) == id(cls2))
