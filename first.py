# coding:utf-8
import random
import string
import base64
import time

list_ex = lambda x: random.sample(
    string.digits + string.ascii_letters + string.punctuation, x)

str_ex = lambda x: ''.join(list_ex(x))


def genstr(l):
    return base64.b32encode(str_ex(l) + str(time.time()))


print genstr(10)
