# coding:utf-8
import operator

listA = [i for i in range(10)]
listB = [i for i in range(10)]

listA.sort(reverse=True)

# listA.append(10)

print listA
print listB

'''
[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
'''
print operator.eq(listA, listB)  # 必须顺序类型全一样，False
# print cmp(listA, listB) # 1
if len(set(listA) - set(listB)) == 0:  # 会去除相同的元素
	print u"一样"

listA.append(10)
print set(listA) - set(listB)  # 10 , 差集 不等于0，代表不一样

print [x for x in listA if x in listB]  # 需要循环列表，性能低，但没有损耗
