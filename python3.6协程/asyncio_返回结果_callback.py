# 事件循环 + 回调（驱动生成器） + epoll(IO 多路复用)

# asyncio 是python 用于解决异步IO编程

# tornado ,gevent
import asyncio,time
from functools import partial

async def get_html(url):
    print("start get nul")
    await asyncio.sleep(2)
    print("end get nul")
    return "finish url"

def callback(url,task):
    print("this is callback",url)


if __name__ == "__main__":
    start_time=time.time()
    loop =asyncio.get_event_loop()

    # task =asyncio.ensure_future(get_html("http://www.baidu.com"))
    task =loop.create_task(get_html("http://www.baidu.com")) # 效果与上面一样
    task.add_done_callback(partial(callback,"http://www.sina.com"))
    loop.run_until_complete(task)
    print(time.time()-start_time)
    print(task.result()) # 得到结果