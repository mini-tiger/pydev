# coding:utf-8
import requests

s=('content', u'PROBLEM\r\nP0\r\nEndpoint:falcon-linux\r\nMetric:net.port.listen\r\nTags:port=8081\r\nmax(#3): 0==0\r\nNote:8081\u4e0d\u901a\r\nMax:3, Current:1\r\nTimestamp:2018-07-12 17:46:00\r\nhttp://127.0.0.1:8081/portal/template/view/1\r\n'), ('tos', u'61566027@163.com'), ('subject', u'[P0][PROBLEM][falcon-linux][][8081\u4e0d\u901a max(#3) net.port.listen port=8081 0==0][O1 2018-07-12 17:46:00]')
ss = dict(s)
print ss
# r = requests.post('http://127.0.0.1:8000/ext/mail', data = ss)
r = requests.post('http://192.168.43.11:8081/ext/mail', data = ss)
print r.url