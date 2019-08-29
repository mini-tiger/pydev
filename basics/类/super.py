# todo 调用父类的方法 ，子类重写父类的方法后，同时又想调用父类的方法时，可以使用
class Animal(object):
    def __init__(self):
        self.color = "白色"

    def eat(self):
        print('eat..........')


class Dog(Animal):
    '重写父类的init'

    def __init__(self):
        super(Dog, self).__init__()  # 调用父类的init方法
        self.name = '狗'

    def eat(self):
        super(Dog, self).eat()
        print('Dog eat........')


d = Dog()
d.eat()
print('一只' + d.color + '的' + d.name)
