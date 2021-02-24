# coding:utf-8
import time
from datetime import timedelta

try:
    from HTMLParser import HTMLParser
    from urlparse import urljoin, urldefrag
except ImportError:
    from html.parser import HTMLParser
    from urllib.parse import urljoin, urldefrag

import asyncio

NORMAL = 0
ERROR = 1
TIMEOUT = 5
concurrency = 10
import socket

now = lambda: time.time()
sem = asyncio.Semaphore(1000)


async def ping(port, ip="192.168.43.14", timeout=1):
    async with sem:
        try:
            # await asyncio.sleep(0
            fut = asyncio.open_connection(ip, port)
            await asyncio.wait_for(fut, timeout=1)
            print("success port:%d" % (port))

        except Exception as e:
            print("port:%d,error:%s" % (port, e))


start = now()
# tasklist = []
# for i in range(10):
tasklist = [ping(port) for port in [1, 2, 3, 3389]]

loop = asyncio.get_event_loop()  # 创建LOOP主线程，所有协程都在这个线程中
# loop.run_until_complete(asyncio.wait(tasklist))
loop.run_until_complete(asyncio.gather(*tasklist)) #与上面一样
print("time:", now() - start)
