# -*- coding: utf-8 -*-
import asyncio
import uvloop
from databases import Database

# xxx  目前 uvloop 只支持 *nix 平台和 Python 3.5。


user = "root"
password = "123456"
port = 3306
hosts = ["192.168.0.1"]  # 500台 db列表


async def query(host):
	DATABASE_URL = f'mysql+pymysql://{user}:{password}@{host}:{port}/mysql?charset=utf8mb4'
	async with Database(DATABASE_URL) as database:
		query = 'select sleep(0.1);'
	rows = await database.fetch_all(query=query)
	print(rows[0])


async def main():
	tasks = [asyncio.create_task(query(host)) for host in hosts]
	await asyncio.gather(*tasks)


# main entrance
if __name__ == '__main__':
	uvloop.install()
	asyncio.run(main())
