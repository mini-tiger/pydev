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


async def ping(port, ip="127.0.0.1", timeout=1):
    try:
        # await asyncio.sleep(0)
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (str(ip), int(port))
        status = cs.connect_ex((address))
        cs.settimeout(timeout)

        # this status is returnback from tcpserver
        if status != NORMAL:
            print("error:,port:%d" % port)
        else:
            print("success:,port:%d" % port)
    except Exception as e:
        print("error:%s,port:%d" % e, port)


start = now()
tasklist = []
for i in range(10):
    tasklist.append(asyncio.ensure_future(ping(i)))

loop = asyncio.get_event_loop()
# task = asyncio.ensure_future(coroutine)
loop.run_until_complete(asyncio.gather(*tasklist))
print(now()-start)
