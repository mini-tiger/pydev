# -*- coding: utf-8 -*-
import requests, json
from models import models
import copy
import logg, os
from requests.exceptions import *
from collections import *

logw = logg.log_class("abc")
bizNT = namedtuple('biz', 'bk_biz_tester bk_biz_productor bk_biz_developer bk_biz_maintainer time_zone bk_biz_name')


class util(object):
	def util_myapi(self, url, method='post', json=None, data=None):
		headers = {'Accept': "application/json"}  ##定义header头，用dict方式定义，即3
		url = url if url.rfind('/', -2) > 0 else url + '/'  # 如果结尾 不是/
		try:
			res = requests.request(method, url, headers=headers, json=json, data=data, timeout=10)
			if res.status_code != 200:
				return {"data": res.text, "ret": 0, "err": "status_code:%d".format(res.status_code)}
			# print dir(res)
			else:
				return {"data": res.text, "ret": 1, "err": None}
		except Exception as e:
			return {"data": "", "ret": 0, "err": e}


def returnHostList(url, **kwargs):
	uu = util()
	# ## views  ex_tasks  put
	j = {
		"bk_app_code": "bk1",
		"bk_app_secret": "c50f40fe-c35b-4a23-89cd-5591b4d55bf0",
		"bk_username": "admin",
	}

	url1 = url  # 源 主机列表
	tmp = copy.deepcopy(models.tmpHostSearch)
	tmp.update(j)
	if kwargs.get("biz"): # 添加BIZ筛选
		bizname = kwargs.get("biz")
		bizfilter = {
			"bk_obj_id": "biz",
			"fields": [],
			"condition": [
				{
					"field": "bk_biz_name",
					"operator": "$eq",
					"value": bizname
				}
			]
		}
	tmp["condition"].append(bizfilter)
	r = uu.util_myapi(url=url1, method='post', json=tmp)  # json=j or data=j

	if r.get("ret") == 0:
		return [], r.get("err")
	# result = r.encode('utf-8')  # 将unicode转换成string

	jd = json.loads(r.get('data'))

	hostData = jd.get('data').get('info')
	# for i in hostData:
	# 	print type(i.get('host')),i
	return hostData, "sucess"


def returnBiz(url, **kwargs):
	uu = util()
	# ## views  ex_tasks  put
	j = {
		"bk_app_code": "bk1",
		"bk_app_secret": "c50f40fe-c35b-4a23-89cd-5591b4d55bf0",
		"bk_username": "admin",
	}

	url1 = url  # 源 主机列表
	tmp = copy.deepcopy(models.tmpBizSearch)
	tmp.update(j)
	r = uu.util_myapi(url=url1, method='post', json=tmp)  # json=j or data=j
	if r.get("ret") == 0:
		return [], r.get("err")

	# result = r.encode('utf-8')  # 将unicode转换成string

	# jd = json.loads(r)
	# print jd
	# length = jd['data']['count']
	Data = r['data']
	result = Data.encode('utf-8')
	jd = json.loads(result)
	# print jd['data']['info']
	return jd['data']['info'], "sucess"


def diffBiz(src, dst):
	tmpSrcdict = {}
	tmpDst = []
	diff = []
	for biz in src:  # 只考虑 源同步到目标，目标比源多的有的不处理
		tbiz = bizNT(biz['bk_biz_tester'], biz['bk_biz_productor'], biz['bk_biz_developer'], biz['bk_biz_maintainer'],
					 biz["time_zone"], biz["bk_biz_name"])
		tmpSrcdict[biz['bk_biz_name']] = tbiz

	for biz in dst:
		tmpDst.append(biz['bk_biz_name'])

	for biz in tmpSrcdict.keys():
		if biz in tmpDst:
			continue
		else:
			diff.append(tmpSrcdict[biz])
	return diff


def addbiz(bizNameTuple):
	uu = util()
	url1 = "http://1.119.132.130:8083/api/v3/biz/0"
	tmp = {
		"bk_biz_name": bizNameTuple.bk_biz_name,
		"bk_biz_maintainer": bizNameTuple.bk_biz_maintainer,
		"bk_biz_productor": bizNameTuple.bk_biz_productor,
		"bk_biz_developer": bizNameTuple.bk_biz_developer,
		"bk_biz_tester": bizNameTuple.bk_biz_tester,
		'time_zone': bizNameTuple.time_zone,
	}
	r = uu.util_myapi(url=url1, method='post', json=tmp)  # json=j or data=j
	if r.get("ret") == 0:
		return [], r.get("err")


def addDstbiz(diff):
	for d in diff:
		addbiz(d)

# bk_cloud_id 没有
hostNT = namedtuple('host','bk_cpu bk_isp_name bk_os_name bk_province_name import_from bk_os_version bk_disk operator \
bk_mem bk_host_name bk_host_innerip bk_comment bk_os_bit bk_outer_mac bk_asset_id bk_service_term bk_sla \
bk_cpu_mhz bk_host_outerip bk_sn bk_os_type bk_mac bk_bak_operator bk_state_name bk_cpu_module')

def returnHostNT(data):
	tmp = hostNT(data['bk_cpu'], data['bk_isp_name'], data['bk_os_name'], data['bk_province_name'], data['import_from'], data['bk_os_version'],
				 data['bk_disk'], data['operator'], data['bk_mem'], data['bk_host_name'], data['bk_host_innerip'], data['bk_comment'], data['bk_os_bit'],
				 data['bk_outer_mac'], data['bk_asset_id'], data['bk_service_term'],data['bk_sla'], data['bk_cpu_mhz'], data['bk_host_outerip'], data['bk_sn'], data['bk_os_type'],
				 data['bk_mac'], data['bk_bak_operator'], data['bk_state_name'], data['bk_cpu_module'])
	return tmp
def diffhost(src,dst):
	addlist=[]
	updatelist=[]
	dellist=[]

	tmpSrcDict={}
	tmpDstDict={}
	for h in src:
		h=h['host']
		tmpSrcDict.setdefault(h['bk_host_innerip'], returnHostNT(h))

	for h in dst:
		h=h['host']
		tmpDstDict.setdefault(h['bk_host_innerip'], returnHostNT(h))

	for ip in tmpSrcDict:
		if ip in tmpDstDict.keys(): # 如果 目标存在 源数据库中的主机IP 比较内容是否相等, 命名元组可以比较
			if tmpDstDict[ip] == tmpSrcDict[ip]:
				continue
			else:
				updatelist.append(tmpSrcDict[ip])
		else:
			addlist.append(tmpSrcDict[ip])

	for ip in tmpDstDict:  # 如果目标库中的主机 在源库中没有，应该删除
		if ip not in tmpSrcDict.keys():
			dellist.append(tmpDstDict[ip])

	return addlist, updatelist, dellist

def addhost():
	uu = util()
	url1 = "http://1.119.132.130:8083/api/v3/hosts/add"

	tmp = copy.deepcopy(models.tmpAddHost)

	r = uu.util_myapi(url=url1, method='post', json=tmp)  # json=j or data=j
	if r.get("ret") == 0:
		return [], r.get("err")
	print r['data']


def returnBizDict(**kwargs):
	uu = util()
	# ## views  ex_tasks  put

	url1 ="http://1.119.132.130:8083/api/v3/biz/search/0"
	tmp = copy.deepcopy(models.tmpBizSearch)
	tmp['fields'].append("bk_biz_id")
	tmp['fields'].append("bk_biz_name")

	if kwargs.get("biz"): # 添加BIZ筛选
		bizname = kwargs.get("biz")
		bizfilter = {
					"bk_biz_name": bizname,
		}
	tmp["condition"].update(bizfilter)

	r = uu.util_myapi(url=url1, method='post', json=tmp)  # json=j or data=j

	if r.get("ret") == 0:
		return [], r.get("err")

	jd = json.loads(r.get('data'))
	#
	return jd.get('data')['info'][0] # {u'bk_biz_id': 3, u'bk_biz_name': u'\u76d1\u63a7\u5e73\u53f0'}
	# # for i in hostData:
	# # 	print type(i.get('host')),i
	# return hostData, "sucess"

def wheel():
	# srcHostList, ok = returnHostList(url='http://paas.gcl-ops.com/api/c/compapi/v2/cc/search_host/',biz="监控平台")
	# if ok != "sucess":
	# 	logw.error(ok)
	# 	os._exit(1)

	##############################################################

	# dstHostList,ok = returnHostList(url= 'http://1.119.132.130:8083/api/v3/hosts/search')
	# if ok != "sucess":
	# 	logw.error(ok)
	# 	os._exit(1)

	# 找出两边的业务
	srcBizList, ok = returnBiz(url='http://paas.gcl-ops.com/api/c/compapi/v2/cc/search_business/')
	if ok != "sucess":
		logw.error(ok)
		os._exit(1)

	dstBizList, ok = returnBiz(url='http://1.119.132.130:8083/api/v3/biz/search/0')
	# print dstBizList
	if ok != "sucess":
		logw.error(ok)
		os._exit(1)

	# 目标业务比源业务少的差异
	diff = diffBiz(srcBizList, dstBizList)
	if diff:  # 业务是否有差别，判断名字
		addDstbiz(diff)

	# 提取每个业务下的主机，比较
	for srcbiz in srcBizList[0:1]:
		# 获取目标库中业务名称与ID 的关系
		dstBizDict=returnBizDict(biz = srcbiz["bk_biz_name"])

		srcHostList, ok = returnHostList(url='http://paas.gcl-ops.com/api/c/compapi/v2/cc/search_host/', biz = srcbiz["bk_biz_name"])
		if ok != "sucess":
			logw.error(ok)
			os._exit(1)
		# for i in  srcHostList:
		# 	print i['host']

		dstHostList, ok = returnHostList(url='http://1.119.132.130:8083/api/v3/hosts/search', biz = srcbiz["bk_biz_name"])
		if ok != "sucess":
			logw.error(ok)
			os._exit(1)

		# for i in srcHostList:
		# 	print i['host']
		# 	print i['host'].keys()
		addlist,updatelist,dellist=diffhost(srcHostList, dstHostList)
	addhost()
if __name__ == "__main__":
	wheel()
