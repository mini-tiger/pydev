# 使用多线程，在协程中集成阻塞IO

import socket
from urllib.parse import urlparse
import asyncio
from concurrent.futures import ThreadPoolExecutor
import requests


def get_url(url):
    data = requests.get(url)
    print(data.text)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor()
    tasks = []
    for i in range(0, 5):
        task = loop.run_in_executor(executor, get_url, "http://www.baidu.com")
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))
