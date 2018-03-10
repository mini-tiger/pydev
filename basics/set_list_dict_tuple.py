# coding:utf-8
from __future__ import print_function
import env


def print_ex(_s, _ss):
    print("{:<36}{}".format(_s, _ss))

print ("{:#^100}".format('''List'''))

l1 = env.list_ex(3)

l2 = [x for x in xrange(10) if x > 3 and x < 5]
print(l1)
print(l2)

print ("{:#^58}".format('''增加'''))
l1 = l1 + l2 + [1, 2, 3, [1, 2, 3]]
print_ex('+,list 相加 :', l1)

l1.extend(l2)
print_ex('extend,列表追加到列表中 :', l1)

l1.append('1')
print_ex('append,追加到列表中 :', l1)

l1.insert(0, 2)
print_ex('insert,根据索引位置插入 :', l1)


print ("{:#^58}".format('''删除'''))
del l1[-1]
print_ex('del,根据索引位置删除  :', l1)

l1.pop(0)
print_ex('pop,同del,并返回元素值:', l1)
l1.remove(4)
print_ex('remove,移除列表中某个值的第一个匹配项:', l1)

print ("{:#^58}".format('''改'''))

l1[0] = 11
print_ex('l1[0],更改索引位置的值 :', l1)


print ("{:#^58}".format('''查'''))
print(l1.index(11))
print_ex('index,返回索引位置的值 :', l1)


print ("{:#^58}".format('''方法'''))

print_ex('count,统计个数 :', l1.count(1))

l1.reverse()
print_ex('reverse,反向 :', l1)

l1.sort()
print_ex('reverse,反向 :', l1)

print ("{:#^100}".format('''Set'''))


s1 = env.set_ex(3)
print(s1)
s2 = {x for x in xrange(2)}
print(s2)

print ("{:#^58}".format('''增加'''))
s1.add(2)
print_ex('add,增加元素 :', s1)


s1.update({2, 3, 4})
print_ex('update,追加元素到集合中 :', s1)

print ("{:#^58}".format('''删除'''))
s1.remove(2)
print_ex('remove,删除元素 :', s1)

print ("{:#^58}".format('''交集，补集，并集'''))
s1 = {x for x in range(10)}
s2 = {x for x in range(10) if x > 6}
print_ex('交集，两个都有 :', s1 & s2)  # s1.union(s2)
print_ex('补集，前面有，后面没有 :', s1 - s2)
print_ex('并集，前面后面的和 :', s1 | s2)
