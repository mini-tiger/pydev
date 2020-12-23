class MyClass:
    # 公共方法
    def getName(self):
        return self.name

    # 公共方法
    def setName(self, name):
        self.name = name
        # 在类的内部可以直接调用私有方法
        self.__outName()

    # 私有方法
    def __outName(self):
        print("Name = {}".format(self.name))


myClass = MyClass()
# 导入inspect模块
import inspect

# 获取MyClass类中所有的方法
methods = inspect.getmembers(myClass, predicate=inspect.ismethod)
print(methods)
# 输出类方法的名称
for method in methods:
    print(method[0])
print("------------")
# 调用setName方法
myClass.setName("Bill")
# 调用getName方法
print(myClass.getName())
# 调用“__outName”方法，这里调用了改完名后的方法，所以可以正常执行
myClass._MyClass__outName()
# 抛出异常，因为“__outName”方法在MyClass类中并不存在
print(myClass.__outName())
