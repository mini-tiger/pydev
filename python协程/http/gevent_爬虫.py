from gevent import monkey

monkey.patch_all()
import gevent
import urllib.request


def run_task(url):
	print('Visit --> %s' % url)
	try:
		response = urllib.request.urlopen(url)
		data = response.read()
		print('%d bytes received from %s.' % (len(data), url))
	except Exception as e:
		print(e)


if __name__ == '__main__':
	urls = ['https://www.baidu.com', 'https://docs.python.org/3/library/urllib.html',
	        'http://www.sina.com.cn']
	greenlets = [gevent.spawn(run_task, url) for url in urls]
	gevent.joinall(greenlets)
