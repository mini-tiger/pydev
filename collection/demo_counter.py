# coding:utf-8
from collections import Counter

cnt = Counter()
for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
	cnt[word] += 1

print cnt
print "==" * 20
cnt1 = Counter("abcabcccddeeadabddadbccc")
print cnt1  # Counter({'c': 7, 'd': 6, 'a': 5, 'b': 4, 'e': 2})
print cnt1.most_common(2)  # most_common() 方法返回最常见的元素及其计数，顺序为最多到最少，输出两个最多字母的 [('c', 7), ('d', 6)]
print cnt1.viewitems()  # dict_items([('a', 5), ('c', 7), ('b', 4), ('e', 2), ('d', 6)])
print cnt1.viewkeys()  # dict_keys(['a', 'c', 'b', 'e', 'd'])

print "==" * 20
c = Counter(a=4, b=1, c=0, d=-1)
print list(c.elements())  # ['a', 'a', 'a', 'a', 'b'] #按照定义的数量生成 指定个字符串

c.subtract(a=1,b=1)# 减去指定个字符串
print list(c.elements()) # ['a', 'a', 'a']