# coding:utf-8
from collections import namedtuple

city = namedtuple('city1', 'name country population')
beijing = city('bj', 'china', 36)
beijing1 = city('bj', 'china', 36)
print(beijing == beijing1) #同样为 true
# b=('bj','china',36)
# beijing1=city._make(b) ##与上面 city('bj','china',36) 作用一样

print(beijing)  ## city(name='bj', country='china', population=36)
print(beijing.name)  # bj
print(beijing[0])  # bj
print(city._fields)  ## ('name', 'country', 'population')

for k, v in beijing._asdict().items():  ## _asdict() 转化为类似 字典格式
	print ('%s : %s ' % (k, v))
'''
name : bj 
country : china 
population : 36 
'''
print( "======" * 20)

point = namedtuple('point', 'x y ')
l = list()
for x in range(1, 10):
	for y in range(1, 10):
		b = (x, y)
		l.append(point._make(b))

print (l, len(l))
