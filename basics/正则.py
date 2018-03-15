# coding:utf-8

import re
import env

s1 = 'aaabbbbbbbabbb213dfdxcx3440-934x' + env.str_ex(10)
print s1

r = re.compile('a')

print re.match(r, s1)


r = re.compile('ab[b?]')

print re.search(r, s1).group()

r = re.compile('[0-9]+')

print re.findall(r, s1)

r = re.compile('a')

print re.sub(r, '', s1)
print re.subn(r, '', s1)