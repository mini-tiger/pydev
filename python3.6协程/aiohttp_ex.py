import aiohttp
import asyncio
import time


conn = aiohttp.TCPConnector(limit=30) # 为了限制同时打开的连接数量
# conn = aiohttp.TCPConnector(limit_per_host=30)#默认是0  时打开限制同时打开连接到同一端点的数量（(host, port, is_ssl) 三的倍数）
# print(dir(conn.connect()))
timeout = aiohttp.ClientTimeout(total=60)
headers = {'content-type': 'application/json'}
async def run(method):
	async with aiohttp.ClientSession(connector=conn, connector_owner=False) as session:
		async with session.request(method,"http://www.baidu.com", headers=headers, timeout=timeout) as resp:
		# async with session.get('http://www.baidu.com',headers=headers,timeout=timeout) as resp:
			# print(resp.status)
			return await resp.text(encoding="utf-8") # 也可以不指定编码
			# print(await resp.json(encoding="utf-8"))


start=time.time()
loop=asyncio.get_event_loop()
tasks=[]
for u in range(3):
	tasks.append(asyncio.ensure_future(run("get")))
aa=loop.run_until_complete(asyncio.wait(tasks))
print(aa[0])
print(len(aa))
loop.close()
conn.close()
print('total {}pages,time cost:{}'.format(len(tasks),time.time()-start))
