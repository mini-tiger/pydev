# -*- coding: utf-8 -*-
import requests, json


class util(object):
	def util_myapi(self, url, method='post', json=None, data=None):
		headers = {'Accept': "application/json"}  ##定义header头，用dict方式定义，即3
		url = url if url.rfind('/', -2) > 0 else url + '/'  # 如果结尾 不是/
		res = requests.request(method, url, headers=headers, json=json, data=data)
		if res.status_code == 500:
			print res
			print dir(res)
		else:
			# res = requests.get(url,headers=headers, auth=('admin','admin' ))
			return res.text


# instance
uu = util()

url = 'http://paas.gcl-ops.com/api/c/compapi/v2/cc/search_host/'

# views ex_tasks   get

# s=uu.util_myapi(url)
# print s




# ## views  ex_tasks  put
j={
    "bk_app_code": "bk1",
    "bk_app_secret": "c50f40fe-c35b-4a23-89cd-5591b4d55bf0",
    "bk_username": "admin",
}



j={
    "bk_app_code": "bk1",
    "bk_app_secret": "c50f40fe-c35b-4a23-89cd-5591b4d55bf0",
    "bk_username": "admin",
    "ip": {
        "data": [],
        "exact": 1,
        "flag": "bk_host_innerip"
    },
    "condition": [
        {
            "bk_obj_id": "host",
            "fields": [],
            "condition": []
        },
        {
            "bk_obj_id": "object",
            "fields": [],
            "condition": [
                {
                    "field": "bk_host_id",
                    "operator": "$neq",
                    "value": 0
                }
            ]
        }
    ],
    "page": {
        "start": 0,
        "limit": 100,
        "sort": "bk_host_name"
    },
    "pattern": ""
}
r=uu.util_myapi(url=url, method='post', json=j)  # json=j or data=j

result = r.encode('utf-8')  #将unicode转换成string

jd = json.loads(result)
print jd
_d= jd['data']['info']
print type(_d)
print len(_d)


# views get_tasks_urlpath
# s = uu.util_myapi(url + 'get_tasks_urlpath/')
# print s
