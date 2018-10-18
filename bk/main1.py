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

# bk_cloud_id 没有  bk_host_id 更新主机用
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

	dstHostIP_ID={}

	for h in src:
		h=h['host']
		tmpSrcDict.setdefault(h['bk_host_innerip'], returnHostNT(h))

	for h in dst:
		h=h['host']
		tmpDstDict.setdefault(h['bk_host_innerip'], returnHostNT(h))
		dstHostIP_ID[h['bk_host_innerip']]=h['bk_host_id']

	for ip in tmpSrcDict:
		if ip in tmpDstDict.keys(): # 如果 目标存在 源数据库中的主机IP 比较内容是否相等, 命名元组可以比较
			if tmpDstDict[ip] == tmpSrcDict[ip]:

				continue
			else:
				# print tmpDstDict[ip]
				# print tmpSrcDict[ip]
				# import time
				# time.sleep(10)
				updatelist.append(tmpSrcDict[ip])
		else:
			addlist.append(tmpSrcDict[ip])

	for ip in tmpDstDict:  # 如果目标库中的主机 在源库中没有，应该删除
		if ip not in tmpSrcDict.keys():
			dellist.append(tmpDstDict[ip])

	return addlist, updatelist, dellist, dstHostIP_ID


def updatehost(host, host_id):
	uu = util()
	url1 = "http://1.119.132.130:8083/api/v3/hosts/batch"

	# tmp = copy.deepcopy(models.tmpAddHost)
	# print host_id,host
	tmphost={"bk_host_id": "%s" %(host_id),
		# "bk_host_innerip": host.bk_host_innerip,  # 更新字段不能包括 IP
					   "import_from": host.import_from,
						"bk_cpu": host.bk_cpu,
					   'bk_isp_name': host.bk_isp_name,
					   'bk_province_name': host.bk_province_name,
					   	'bk_os_name': host.bk_os_name,
					   'bk_os_version': host.bk_os_version,
					   'bk_disk': host.bk_disk,
					   'operator': host.operator,
					    'bk_mem': host.bk_mem,
					   'bk_host_name': host.bk_host_name,
					   'bk_comment': host.bk_comment,
					   'bk_os_bit': host.bk_os_bit,
					   'bk_outer_mac': host.bk_outer_mac,
					   'bk_asset_id': host.bk_asset_id,
					   'bk_service_term': host.bk_service_term,
					   'bk_os_type': host.bk_os_type,
					   'bk_mac': host.bk_mac,
					   'bk_bak_operator': host.bk_bak_operator,
					   'bk_state_name': host.bk_state_name,
					   'bk_cpu_module': host.bk_cpu_module,
					    'bk_sla': host.bk_sla,
					   'bk_cpu_mhz': host.bk_cpu_mhz,
					   'bk_host_outerip': host.bk_host_outerip,
					   'bk_sn': host.bk_sn,
					   }
	# print tmphost
	r = uu.util_myapi(url=url1, method='put', json=tmphost)  # json=j or data=j
	if r.get("ret") == 0:
		return [], r.get("err")
	print r['data']

def addhost(host,biz_id):
	uu = util()
	url1 = "http://1.119.132.130:8083/api/v3/hosts/add"

	tmp = copy.deepcopy(models.tmpAddHost)
	tmphost={"bk_host_innerip": host.bk_host_innerip,
					   "import_from": host.import_from,
						"bk_cpu": host.bk_cpu, # 防止CPU为0
					   'bk_isp_name': host.bk_isp_name,
					   'bk_province_name': host.bk_province_name,
					   	'bk_os_name': host.bk_os_name,
					   'bk_os_version': host.bk_os_version,
					   'bk_disk': host.bk_disk,
					   'operator': host.operator,
					    'bk_mem': host.bk_mem,
					   'bk_host_name': host.bk_host_name,
					   'bk_comment': host.bk_comment,
					   'bk_os_bit': host.bk_os_bit,
					   'bk_outer_mac': host.bk_outer_mac,
					   'bk_asset_id': host.bk_asset_id,
					   'bk_service_term': host.bk_service_term,
					   'bk_os_type': host.bk_os_type,
					   'bk_mac': host.bk_mac,
					   'bk_bak_operator': host.bk_bak_operator,
					   'bk_state_name': host.bk_state_name,
					   'bk_cpu_module': host.bk_cpu_module,
					    'bk_sla': host.bk_sla,
					   'bk_cpu_mhz': host.bk_cpu_mhz,
					   'bk_host_outerip': host.bk_host_outerip,
					   'bk_sn': host.bk_sn,
					   }

	tmp["host_info"]["0"].update(tmphost)
	tmp["bk_biz_id"]=biz_id
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
		addDstbiz(diff) # 先保证业务一样

	# 提取每个业务下的主机，比较源库与目标库中 每个业务中的主机
	for srcbiz in srcBizList:
		# 获取目标库中业务名称与ID 的关系
		dstBizDict=returnBizDict(biz = srcbiz["bk_biz_name"]) # 提取目标业务 的ID与名字的关系 ，添加目标库中的主机要用

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
		addlist,updatelist,dellist, dsthostipid =diffhost(srcHostList, dstHostList)


		print srcbiz["bk_biz_name"]
		# print len(addlist),addlist
		print len(updatelist)
		for i in updatelist:
			print i.bk_cpu,i.bk_host_innerip
		# print len(dellist),dellist


		for host in addlist:
			addhost(host,dstBizDict['bk_biz_id'])

		for host in updatelist:
			updatehost(host,dsthostipid[host.bk_host_innerip]) # 更新需要知道  主机ID

		import time
		time.sleep(5)
if __name__ == "__main__":
	wheel()
