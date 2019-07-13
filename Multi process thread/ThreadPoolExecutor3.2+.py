import time
from concurrent.futures import ThreadPoolExecutor


# 可回调的task
def pub_task(msg):
	time.sleep(3)
	return msg


# 创建一个线程池
pool = ThreadPoolExecutor(max_workers=3)

# 往线程池加入2个task
task1 = pool.submit(pub_task, 'a')
task2 = pool.submit(pub_task, 'b')

print(task1.done())  # False
time.sleep(4)
print(task2.done())  # True

print(task1.result())
print(task2.result())
print("*" * 100)
import requests

URLS = ['http://www.csdn.com', 'http://qq.com', 'http://www.leasonlove.cn']


def task(url, timeout=10):
	return requests.get(url, timeout=timeout)


pool = ThreadPoolExecutor(max_workers=3)
results = pool.map(task, URLS)  # map方法是创建一个迭代器，回调的结果有序放在迭代器中。

for ret in results:
	print('%s, %s' % (ret.url, ret))
