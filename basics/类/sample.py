# coding:utf-8
class cc(object):
    n = 0  #记录被调用次数
    def __new__(cls):
        cls.a = 0

        # print cls.n
        return super(cc, cls).__new__(cls)

    def __init__(self):
        self.aaa = 1
        cc.n += 1

    def aa(self):
        return 1


print cc().__class__.__name__  # cc
print cc().a  # 0
print cc().aa()  # 1
print dir(cc)  # [...., 'a', 'aa', 'n']
abc = cc()
abc1 = cc()
print cc.n   ##调用5次
