# coding:utf-8
import string,random

#列表字典
def create_str(n):
	_l=random.sample(string.letters+string.digits,n)
	return ''.join(_l)

#建立
print [x for x in range(10) if x%2 !=1]
print {x:y for x in range(10) for y in range(10)}
print dict([(x,x+1) for x in range(10)])


l1=create_str(8)
l2=create_str(8)
print l1    ##u7LF6VdT
l1=''.join(sorted(l1))
print l1    ##67FLTVdu

l3=zip(l1, l2) 
print l3   #[('D', 'w'), ('P', 'n'), ('T', 'P'), ('Z', 'V'), ('a', 'A'), ('b', 'l'), ('q', 'S'), ('t', 'F')]
d1=dict(l3)
print d1   #{'Q': 'P', 'E': 'U', 'I': 'v', '1': '2', '5': 'n', 'w': 'S', 'v': 'm', 'Z': 'H'}

  #排序
d2=sorted(d1.iteritems(),key=lambda x:x[1]) 
print d2 ##[('P', '1'), ('A', 'B'), ('0', 'H'), ('C', 'O'), ('j', 'Q'), ('b', 'R'), ('i', 'i'), ('H', 'm')]
d3=dict(d2) 
print d3 #{'E': 'q', 'j': 'K', 'p': '3', 'r': '8', 'T': 'a', 'W': 'n', '8': 'U', '2': '0'}

#追加
d3.update({'a':3}) #{'a': 3, 'E': '9', 'f': '7', 'm': 'v', '1': 'z', '3': 'F', '5': 'U', 'w': 'J', 'v': 'E'}
print d3

print [1]+[2] #[1, 2]
l=[1]
l.extend([2])
print l #[1, 2]

#删除
print d3.pop('a') ##删除key,返回删除key的vaule

#del d3['a']
l.pop(0)   #索引
print l  #[2]
l.extend([1])
l.remove(1)  #值
print l   #[2]


#更改
dd={'a':1}
dd['a']=2
print dd   #{'a': 2}
l=[1,2]
l[0]=2
print l   #[2, 2]


#字典
dd={'a':1}
print dd
print dd.has_key('a')
dd.setdefault('b', 2)
print dd

#列表
l=[x for x in range(3)]
l.insert(0, 7)   #索引位置插入
print l
l.append(4)   #追加
print l

print l.count(1)  ##统计有多少是1 的项


##function
def func1(*a,**k):
	print a
	print k


f1=func1(1,2,[1,2],a=1)

#iter gen

def gen(n):
	while True:
		if n>0:
			yield n
			n=n-1
		else:
			raise StopIteration

g=gen(2)
print g.next()
print g.next()
try:
	g.next()
except StopIteration as e:
	pass

class iter_tools(object):
	def __init__(self):
		self.n=3

	def __iter__(self):
		return

	def next(self):
		if self.n>0:
			self.n=self.n-1
			return self.n
		else:
			return StopIteration

i=iter_tools()
print i.next()
print i.next()
print i.next()
print i.next()

#装饰器

def wrapp(a):
	def bibao1(func):
		def bibao(n):
			print '%d %5d %s' %(a,func(n),3)
		return bibao
	return bibao1
@wrapp(a=1)
def func1(n):
	return n

f1=func1(2) #1 2 3

#类
class cls1(object):
	def __init__(self,*a,**w):
		super(cls1,self).__init__()

	def c(self):
		return 1

cc1=cls1(1,[1,2],a=1)
print cc1.c()

class cls2(object):
	def __news__(cls,*a,**w):
		if not hasattr(cls2, 'i'):
			cls2.i=super(cls2, cls).__news__(cls,*a,**w)
	def __init__(self,*a,**w):
		pass
	def c(self):
		return 1

	def __getattr__(self,k):
		return k

	def __setattr__(self,k,v):
		self.__dict__[k]=v

	def __call__(self,k):
		return self.k

	@property
	def c1(self):
		return 11


cc2=cls2(1,a=1)
print cc2.c() #1
cc2.a=1
print hasattr(cc2, 'a') #True

print cc2('a') #k
print cc2.c1 # 11

#lambda
import time
func2=lambda x:time.time()
print func2(1)
func2=lambda :time.time()
print func2()

#string
create_list= lambda x: random.sample(string.letters+string.digits,x)
l1=create_list(8)
print l1 #['E', 'i', '0', 'B', 'W', 'U', 'G', 'f']
s1=''.join(l1)
s1=s1+'a'+'b'
print s1 #Ei0BWUGfab
#s1.replace(old, new, count)
print s1.split('a') #['Ei0BWUGf', 'b']
print s1.strip('abcdefg') 
str=s1 #zJeU3xEm

#全部大写：str.upper()
#全部小写：str.lower()
#大小写互换：str.swapcase()
#首字母大写，其余小写：str.capitalize()
#首字母大写：str.title()
print '%s lower=%s' % (str,str.lower())
print '%s upper=%s' % (str,str.upper())
print '%s swapcase=%s' % (str,str.swapcase())
print '%s capitalize=%s' % (str,str.capitalize())
print '%s title=%s' % (str,str.title())


#map
l=[x for x in range(10)]
l1=map(lambda x:x+1, l)
print l1
l2=filter(lambda x:x>5, l1)
print l2


#itertool
import itertools
a=[1,2,1,2]
b={'a':1}
# print enumerate(a).next()
# print enumerate(b).next()
for x,y in  itertools.groupby(enumerate([1,2]),key=lambda x:x>1):
	print x
	print list(y)