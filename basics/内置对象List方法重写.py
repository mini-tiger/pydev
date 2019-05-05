class ListNew(list):
    def __init__(self):
        super(ListNew, self).__init__()  # 执行父类中的代码，并将父类产生的属性 继承

    def diy(self, v):
        return self.count(v)

    def count(self, v):
        print("重写继承count方法")
        return super(ListNew, self).count(v)  # 执行父类中的代码，并将父类产生的属性 继承


if __name__ == "__main__":
    l1 = ListNew()

    print(l1.__dir__())
    l1.append(1)
    print(l1)
    print("count func:", l1.count(1))
    print("diy func:", l1.diy(1))
