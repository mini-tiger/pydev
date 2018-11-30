import aiohttp
import asyncio
import time, copy, json, os
from models import models # 相对路径导入，提示报错正常
import logg
from concurrent.futures._base import TimeoutError
from collections import *
log = logg.Logger()
logw = log.returnlog()

loop = asyncio.get_event_loop()
conn = aiohttp.TCPConnector(limit=30)  # 为了限制同时打开的连接数量
# conn = aiohttp.TCPConnector(limit_per_host=30)#默认是0  时打开限制同时打开连接到同一端点的数量（(host, port, is_ssl) 三的倍数）
bizNT = namedtuple('biz', 'bk_biz_tester bk_biz_productor bk_biz_developer bk_biz_maintainer time_zone bk_biz_name')
timeout = aiohttp.ClientTimeout(total=15)
headers = {'Accept': "application/json"}
dstUrlSuffix = "http://1.119.132.155:8083"
srcUrlsuffix = "http://paas.gcl-ops.com/"

async def run(method, url, json=None):
	async with aiohttp.ClientSession(connector=conn, connector_owner=False) as session:
		try:
			async with session.request(method, url, headers=headers, timeout=timeout, data=json) as resp:
				# async with session.get('http://www.baidu.com',headers=headers,timeout=timeout) as resp:
				_d = await resp.text(encoding="utf-8")
				if resp.status == 200:
					return {"data": _d, "ret": 1, "err": None}  # 也可以不指定编码
				else:
					return {"data": _d, "ret": 0, "err": resp.status}
			# print(await resp.json(encoding="utf-8"))
		except TimeoutError as e:
			return {"data": None, "ret": 0, "err": "%s request timeout" % (url)}

def returnBiz(**kwargs):

	j = {
		"bk_app_code": "bk1",
		"bk_app_secret": "c50f40fe-c35b-4a23-89cd-5591b4d55bf0",
		"bk_username": "admin",
	}

	tmp = copy.deepcopy(models.tmpBizSearch)
	tmp.update(j)
	# print(tmp)
	coroutine1 = run("post", url=srcUrlsuffix + '/api/c/compapi/v2/cc/search_business/', json=json.dumps(tmp))
	coroutine2 = run("post", url=dstUrlSuffix + '/api/v3/biz/search/0', json=json.dumps(tmp))

	srcBiz = loop.create_task(coroutine1)
	dstBiz = loop.create_task(coroutine2)
	loop.run_until_complete(asyncio.wait([srcBiz, dstBiz]))

	if srcBiz.result().get("ret") == 0:
		logw.error(srcBiz.result().get("err"))
		os._exit(1)
	_dSrc = json.loads(srcBiz.result().get("data"))

	if _dSrc.get("result") != True:
		logw.error(_dSrc.get("message"))
		os._exit(1)

	_dDst = json.loads(dstBiz.result().get("data"))
	if dstBiz.result().get("ret") == 0:
		logw.error(dstBiz.result().get("err"))
		os._exit(1)

	if _dDst.get("result") != True:
		logw.error(_dSrc.get("bk_error_msg"))
		os._exit(1)
	return _dSrc["data"]["info"],  _dDst["data"]["info"]

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

def addbiz(diff):
	url1 = dstUrlSuffix + "/api/v3/biz/0"
	tasks = []
	for bizNameTuple in diff:
		tmp = {
			"bk_biz_name": bizNameTuple.bk_biz_name,
			"bk_biz_maintainer": bizNameTuple.bk_biz_maintainer,
			"bk_biz_productor": bizNameTuple.bk_biz_productor,
			"bk_biz_developer": bizNameTuple.bk_biz_developer,
			"bk_biz_tester": bizNameTuple.bk_biz_tester,
			'time_zone': bizNameTuple.time_zone,
		}
		tasks.append(asyncio.ensure_future(run("post" ,url=url1, json=json.dumps(tmp))))
	# r = uu.util_myapi(url=url1, method='post', json=tmp)  # json=j or data=j
	taskResult = loop.run_until_complete(asyncio.gather(*tasks))
		# if r.get("ret") == 0:
		# 	return [], r.get("err")
	# print(taskResult)
	for t in taskResult:
		if t.get("ret") == 0:
			logw.error(t.get("err"))
			continue

		_d = json.loads(t.get("data"))
		if _d["result"] != True:
			logw.error(_d.get("bk_error_msg"))

		else:
			logw.info("sucess add bizid %s" % (_d.get("data").get("bk_biz_id")))

def addDstbiz(diff):
	# for d in diff:
		addbiz(diff)

async def returnBizDict(**kwargs):

	url1 = dstUrlSuffix + "/api/v3/biz/search/0"
	tmp = copy.deepcopy(models.tmpBizSearch)
	tmp['fields'].append("bk_biz_id")
	tmp['fields'].append("bk_biz_name")

	if kwargs.get("biz"):  # 添加BIZ筛选
		bizname = kwargs.get("biz")
		bizfilter = {
			"bk_biz_name": bizname,
		}
		tmp["condition"].update(bizfilter)

	task = asyncio.ensure_future(run("post", url=url1, json=json.dumps(tmp)))

	taskResult = await asyncio.gather(task)  # 协程嵌套，这里是 await

	t= taskResult[0]
	if t.get("ret") == 0:
		logw.error(t.get("err"))
		os._exit(1)

	_d = json.loads(t.get("data"))
	if _d["result"] != True:
		logw.error(_d.get("bk_error_msg"))
		os._exit(1)
	# print(_d["data"])
	return _d["data"]["info"][0]


async def returnHostList(url, **kwargs):

	# ## views  ex_tasks  put
	j = {
		"bk_app_code": "bk1",
		"bk_app_secret": "c50f40fe-c35b-4a23-89cd-5591b4d55bf0",
		"bk_username": "admin",
	}

	url1 = url  # 源 主机列表
	tmp = copy.deepcopy(models.tmpHostSearch)
	tmp.update(j)
	if kwargs.get("biz"):  # 添加BIZ筛选
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

	task = asyncio.ensure_future(run("post", url=url1, json=json.dumps(tmp)))
	taskResult = await asyncio.gather(task)  # 协程嵌套，这里是 await
	# print(taskResult)
	t = taskResult[0]
	if t.get("ret") == 0:
		logw.error(t.get("err"))
		return []
		# os._exit(1)


	_d = json.loads(t.get("data"))
	if _d["result"] != True:
		logw.error(_d.get("bk_error_msg"))
		# os._exit(1)
	# print(_d["data"])
	# print(_d["data"]["info"])
	return _d["data"]["info"]


hostNT = namedtuple('host', 'bk_cpu bk_isp_name bk_os_name bk_province_name import_from bk_os_version bk_disk operator \
bk_mem bk_host_name bk_host_innerip bk_comment bk_os_bit bk_outer_mac bk_asset_id bk_service_term bk_sla \
bk_cpu_mhz bk_host_outerip bk_sn bk_os_type bk_mac bk_bak_operator bk_state_name bk_cpu_module')

def returnHostNT(data):
	tmp = hostNT(data['bk_cpu'], data['bk_isp_name'], data['bk_os_name'], data['bk_province_name'], data['import_from'],
				 data['bk_os_version'],
				 data['bk_disk'], data['operator'], data['bk_mem'], data['bk_host_name'], data['bk_host_innerip'],
				 data['bk_comment'], data['bk_os_bit'],
				 data['bk_outer_mac'], data['bk_asset_id'], data['bk_service_term'], data['bk_sla'], data['bk_cpu_mhz'],
				 data['bk_host_outerip'], data['bk_sn'], data['bk_os_type'],
				 data['bk_mac'], data['bk_bak_operator'], data['bk_state_name'], data['bk_cpu_module'])
	return tmp



def diffhost(src, dst):
	addlist = []
	updatelist = []
	dellist = []

	tmpSrcDict = {}
	tmpDstDict = {}

	dstHostIP_ID = {}

	for h in src:
		h = h['host']
		tmpSrcDict.setdefault(h['bk_host_innerip'], returnHostNT(h))

	for h in dst:
		h = h['host']
		tmpDstDict.setdefault(h['bk_host_innerip'], returnHostNT(h))
		dstHostIP_ID[h['bk_host_innerip']] = h['bk_host_id']

	for ip in tmpSrcDict:
		if ip in tmpDstDict.keys():  # 如果 目标存在 源数据库中的主机IP 比较内容是否相等, 命名元组可以比较
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
		if ip not in tmpSrcDict.keys() and "10.240" in ip:
			dellist.append(tmpDstDict[ip])

	return addlist, updatelist, dellist, dstHostIP_ID

async def addhost(host, biz_id):
	url1 = dstUrlSuffix + "/api/v3/hosts/add"

	tmp = copy.deepcopy(models.tmpAddHost)
	tmphost = {"bk_host_innerip": host.bk_host_innerip,
			   "import_from": host.import_from,
			   "bk_cpu": host.bk_cpu,  # 防止CPU为0
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
	tmp["bk_biz_id"] = biz_id

	task = asyncio.ensure_future(run("post", url=url1, json=json.dumps(tmp)))
	taskResult = await asyncio.gather(task)  # 协程嵌套，这里是 await

	t = taskResult[0]
	if t.get("ret") == 0:
		logw.error("addhost ip:%s error:%s" % (host.bk_host_innerip, t.get("err")))
		return []
		# os._exit(1)

	_d = json.loads(t.get("data"))
	# print(_d)
	if _d["result"] != True:
		# logw.error(_d.get("bk_error_msg"))
		logw.error(u"addhost ip:%s error:%s" % (host.bk_host_innerip, _d['bk_error_msg']))
		return []
		# os._exit(1)
	# print(_d["data"])
	# print(_d["data"]["info"])
	return _d["data"]

async def updatehost(host, host_id):

	url1 = dstUrlSuffix + "/api/v3/hosts/batch"

	tmphost = {"bk_host_id": "%s" % (host_id),
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
	# print(tmphost)
	task = asyncio.ensure_future(run("put", url=url1, json=json.dumps(tmphost)))
	taskResult = await asyncio.gather(task)  # 协程嵌套，这里是 await

	t = taskResult[0]
	# print(taskResult)
	if t.get("ret") == 0:
		logw.error("updatehost ip:%s error:%s" % (host.bk_host_innerip, t.get("err")))
		return []
		# os._exit(1)

	_d = json.loads(t.get("data"))
	# print(_d)
	if _d["result"] != True:
		# logw.error(_d.get("bk_error_msg"))
		logw.error(u"upatehost ip:%s error:%s" % (host.bk_host_innerip, _d['bk_error_msg']))
		return []
		# os._exit(1)
	# print(_d["data"])
	# print(_d["data"]["info"])
	return _d["data"]

def wheel():

	srcBizList, dstBizList = returnBiz()
	# print(srcBizList)
	# print(dstBizList)

	diff = diffBiz(srcBizList, dstBizList)
	# print(diff)
	if diff:  # 业务是否有差别，判断名字
		addDstbiz(diff)  # 先保证业务一样

	# 获取目标库中业务名称与ID 的关系
	# dstBizDict = returnBizDict()  # 提取目标业务 的ID与名字的关系 ，添加目标库中的主机要用
	# print(dstBizDict)

	for srcbiz in srcBizList:
		# print(srcbiz.get("bk_biz_name"))
		# 三个一起执行，协程嵌套
		dstBizDictT = asyncio.ensure_future(returnBizDict(biz=srcbiz["bk_biz_name"]))
		srcHostListT = asyncio.ensure_future(returnHostList(url=srcUrlsuffix + 'api/c/compapi/v2/cc/search_host/', biz=srcbiz["bk_biz_name"]))
		dstHostListT = asyncio.ensure_future(returnHostList(url=dstUrlSuffix + '/api/v3/hosts/search', biz=srcbiz["bk_biz_name"]))

		# loop1 = asyncio.new_event_loop()
		# dstBizDict = loop1.create_task(dstBizDictTask)
		# srcHostList = loop1.create_task(srcHostListTask)
		# dstHostList = loop1.create_task(dstHostListTask)

		loop.run_until_complete(asyncio.gather(*[dstBizDictT, srcHostListT,dstHostListT]))  # 阻塞主进程
		dstBizDict =  dstBizDictT.result()
		srcHostList = srcHostListT.result()
		dstHostList = dstHostListT.result()
		# print(dstBizDict)
		for i in srcHostList:
			print(i)


		addlist, updatelist, dellist, dsthostipid = diffhost(srcHostList, dstHostList)
		# print(addlist)
		# print(updatelist)
		tasks = []
		for host in addlist:
			logw.info(u"biz:%s,[addhost] ip:%s" % (srcbiz["bk_biz_name"], host.bk_host_innerip))
			tasks.append(addhost(host, dstBizDict['bk_biz_id']))

		for host in updatelist:
			if host.bk_cpu == 0 or host.bk_cpu_mhz == 0:
					logw.warn(u"跳过 ip:%s, biz: %s, host_id:%d,bk_cpu or bk_cpu_mh 是0" % (host.bk_host_innerip,srcbiz["bk_biz_name"], dsthostipid[host.bk_host_innerip]))
					continue
			logw.info(u"biz:%s,[updatehost] ip:%s" % (srcbiz["bk_biz_name"], host.bk_host_innerip))
			tasks.append(updatehost(host, dsthostipid[host.bk_host_innerip]))

		loop.run_until_complete(asyncio.gather(*tasks))  # 阻塞主进程

if __name__ == "__main__":
	wheel()

	loop.close()
	conn.close()