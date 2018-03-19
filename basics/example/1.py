# coding:utf-8

ti = '''题目:有四个数字：1、2、3、4，能组成多少个互不相同且无重复数字的三位数？各是多少？'''
print("{:<106}".format(ti))

# 方法一
l = []
for i in xrange(1, 5):
    for m in xrange(1, 5):
        for n in xrange(1, 5):
            if i != m and i != n and m != n:
                l.append(i * 100 + m * 10 + n)
print l

# 方法二
list_num = xrange(1, 5)
l = [i * 100 + j * 10 +
     k for i in list_num for j in list_num for k in list_num if (j != i and k != j and k != i)]

print l

from itertools import permutations
l = permutations(xrange(1, 5), 3)  # (1,2,3),(1,2,4)....
print map(lambda (x, y, z): x * 100 + y * 10 + z, l)

print
print
ti = '''题目：企业发放的奖金根据利润提成。利润(I)低于或等于10万元时，奖金可提10%；利润高于10万元，低于20万元时，低于10万元的部分按10%提成，高于10万元的部分，可提成7.5%；20万到40万之间时，高于20万元的部分，可提成5%；40万到60万之间时高于40万元的部分，可提成3%；60万到100万之间时，高于60万元的部分，可提成1.5%，高于100万元时，超过100万元的部分按1%提成，从键盘输入当月利润I，求应发放奖金总数？ '''
print("{:<106}".format(ti))

x = 500001  # 利润

if x <= 100000:
    bonus = x * 0.1
    print u"奖金:", bonus, u"元"
elif 100001 < x <= 200000:
    bonus = 10000 + (x - 100000) * 0.075
    print u"奖金:", bonus, u"元"
elif 200001 < x <= 400000:
    bonus = 10000 + 7500 + (x - 200000) * 0.05
    print u"奖金:", bonus, u"元"
elif 400001 < x <= 600000:
    bonus = 10000 + 7500 + 10000 + (x - 400000) * 0.03
    print u"奖金:", bonus, u"元"
elif 600001 < x <= 1000000:
    bonus = 10000 + 7500 + 10000 + 6000 + (x - 600000) * 0.015
    print u"奖金:", bonus, u"元"
elif 600001 < x <= 1000000:
    bonus = 10000 + 7500 + 10000 + 6000 + 6000 + (x - 600000) * 0.01
    print u"奖金:", bonus, u"元"

print
print
ti = '''题目：输入某年某月某日，判断这一天是这一年的第几天？'''
print("{:<106}".format(ti))
# 方法一
import time
import datetime
d = '2017-1-5'

timeArray = time.strptime(d, "%Y-%m-%d")

d1 = d.split('-')  # 转换为2017-1-1
d1[1] = '1'
d1[2] = '1'
d1 = '-'.join(d1)

timeArray1 = time.strptime(d1, "%Y-%m-%d")
tt = int(time.mktime(timeArray))
tt1 = int(time.mktime(timeArray1))

print(tt - tt1) / 86400 + 1

# 方法二
t = time.strptime(d, "%Y-%m-%d")
print time.strftime("今年的第%j天", t)  # %j  一年第几天


print
print
ti = '输入三个整数x,y,z，请把这三个数由小到大输出'
print("{:<106}".format(ti))

x = 2
y = 1
z = 100
l = [x, y, z]
l.sort()


ti = '输出 9*9 乘法口诀表'
print("{:<106}".format(ti))
# 方法一
for i in xrange(1, 10):
    print
    for j in xrange(1, i + 1):
        print '{0} * {1} = {2} ;'.format(i, j, i * j),
print
print
ti = '打印出所有的"水仙花数"，所谓"水仙花数"是指一个三位数，其各位数字立方和等于该数本身。例如：153是一个"水仙花数"，因为153=1的三次方＋5的三次方＋3的三次方。'
print("{:<106}".format(ti))

for i in range(100, 999):
    b = str(i)[0]
    s = str(i)[1]
    g = str(i)[2]
    if int(b)**3 + int(s)**3 + int(g)**3 == i:
        print i

print
print
ti = '输入一行字符，分别统计出其中英文字母、空格、数字和其它字符的个数'
print("{:<106}".format(ti))
#方法一
s = '111111112dsfxfdhndfxfdftt33123  d e13'

import re
r = re.compile('[0-9]')
print 'digits {} '.format(str(len(re.findall(r, s))))


r = re.compile('[a-zA-Z]')
print 'ascii_letters {} '.format(str(len(re.findall(r, s))))


r = re.compile('\s')
print '空格 {} '.format(str(len(re.findall(r, s))))
#方法二
letters = 0
space = 0
others = 0
digit = 0

for c in s:
    if c.isalpha():
        letters += 1
    elif c.isspace():
        space += 1
    elif c.isdigit():
        digit += 1
    else:
        others += 1

print 'digit {} ,letters {},space {}'.format(digit, letters, space)

ti = '求s=a+aa+aaa+aaaa+aa...a的值，其中a是一个数字。例如2+22+222+2222+22222(此时共有5个数相加)，几个数相加由键盘控制'

print
print
print("{:<106}".format(ti))

s = '2'
n = 5 #('几位叠加:')
#方法一
ss=0
for i in xrange(1,n+1):
    _s = s * int(i)
    print '数字: {}'.format(_s)
    ss+=int(_s)

print 'result : {}'.format(ss)

#方法二
_l=[]
for i in xrange(1,n+1):
    _s = s * int(i)
    print '数字: {}'.format(_s)
    _l.append(int(_s))

print 'result : {}'.format(sum(_l))