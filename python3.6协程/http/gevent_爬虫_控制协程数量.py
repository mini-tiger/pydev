from gevent import monkey, pool
import time
monkey.patch_all()
import gevent
import urllib.request

jobs = []
links = []
p = pool.Pool(1)


def run_task(url):
	print('Visit --> %s' % url)
	try:
		response = urllib.request.urlopen(url)
		data = response.read()
		print('%d bytes received from %s.' % (len(data), url))
	except Exception as e:
		print(e)


if __name__ == '__main__':
	b=time.time()
	urls = ['http://www.sina.com.cn', 'https://www.baidu.com', 'https://docs.python.org/3/library/urllib.html']

	jobs = [p.spawn(run_task, url) for url in urls]
	gevent.joinall(jobs)
	print(time.time()-b)