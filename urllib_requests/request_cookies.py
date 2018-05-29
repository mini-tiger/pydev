# -*- coding: utf-8 -*-
import requests
import http.cookiejar as cookielib


def save_cookies1():
	session = requests.Session()
	session.cookies = cookielib.LWPCookieJar(filename="cookie.txt")

	response = session.get("https://www.baidu.com", headers=headers)

	session.cookies.save(ignore_discard=True, ignore_expires=True)


def save_cookies2():
	session = requests.session()
	session.cookies = cookielib.LWPCookieJar(filename='cookie.txt')  ##由于没有登录信息，都是success
	try:
		print dir(session.cookies)
		session.cookies.load(ignore_discard=True)
	except:
		print(u"Cookie 未能加载")


	url = "https://www.baidu.com/"
	login_code = session.get(url, headers=headers, allow_redirects=False).status_code
	if login_code == 200:
		print "success"
	else:
		print "Fail"

if __name__ == '__main__':
	agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.1.2.3000 Chrome/55.0.2883.75 Safari/537.36'
	headers = {
		# "Host": "https://www.baidu.com/",
		'User-Agent': agent
	}
	save_cookies1()
	save_cookies2()
