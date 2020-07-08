d = dict()


class A():
    def __init__(self):
        pass


a = A()
print(d.update({1: a}))

for k, v in d.items():
    print(k,type(v) )
