class FooParent1(object):
    def __init__(self):
        self.parent = 'I\'m the parent1.'
        print('Parent')

    def bar(self, message):
        print("%s from Parent1" % message)

    def parent1(self):
        print("this is parent1")


class FooParent2(object):
    def __init__(self):
        self.parent = 'I\'m the parent2.'
        print('Parent2')

    def bar(self, message):
        print("%s from Parent2" % message)

    def parent2(self):
        print("this is parent2")


class FooChild(FooParent1, FooParent2):  # todo 顺序决定  继承了谁的同名方法
    def __init__(self):
        # super(FooChild,self) 首先找到 FooChild 的父类（就是类 FooParent），然后把类B的对象 FooChild 转换为类 FooParent 的对象
        super(FooChild, self).__init__()  # 执行父类中的代码，并将父类产生的属性 继承
        # FooParent2.__init__(self)
        print('Child')

    def bar(self, message):
        super(FooChild, self).bar(message)  # 执行父类中的代码，并将父类产生的属性 继承
        print('Child bar fuction')
        print(self.parent)


if __name__ == '__main__':
    fooChild = FooChild()
    fooChild.bar('HelloWorld')
    print("parent" in fooChild.__dir__())
    print("parent1" in fooChild.__dir__())

'''
result:

Parent
Child
HelloWorld from Parent
Child bar fuction
I'm the parent.
'''
