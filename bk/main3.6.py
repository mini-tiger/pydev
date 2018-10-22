import aiohttp
import asyncio
import time, copy, json
from bk.models import models
from concurrent.futures._base import TimeoutError

conn = aiohttp.TCPConnector(limit=30)  # 为了限制同时打开的连接数量
# conn = aiohttp.TCPConnector(limit_per_host=30)#默认是0  时打开限制同时打开连接到同一端点的数量（(host, port, is_ssl) 三的倍数）
# print(dir(conn.connect()))
timeout = aiohttp.ClientTimeout(total=10)
headers = {'Accept': "application/json"}


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
			return {"data": None, "ret": 0, "err": e}

def returnBiz(loop, **kwargs):
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

	task1 = loop.create_task(coroutine1)
	task2 = loop.create_task(coroutine2)
	loop.run_until_complete(asyncio.wait([task1, task2]))

	loop.close()
	conn.close()

	print(task1.result())
	print(task2.result())


dstUrlSuffix = "http://1.119.132.155:8083"
srcUrlsuffix = "http://paas.gcl-ops.com/"


def wheel():
	loop = asyncio.get_event_loop()

	returnBiz(loop)


# print('total {}pages,time cost:{}'.format(len(tasks),time.time()-start))

if __name__ == "__main__":
	wheel()
