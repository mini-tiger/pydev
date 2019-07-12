# coding:utf-8
import time
import asyncio

now = lambda: time.time()
sem = asyncio.Semaphore(1000)

ListAll = []


async def GenNum(max):
    async with sem:
        ListAll.append([x for x in range(max)])


start = now()
# tasklist = []
# for i in range(10):
tasklist = [GenNum(max) for max in range(1,11000)]
# print(tasklist)
loop = asyncio.get_event_loop()  # 创建LOOP主线程，所有协程都在这个线程中
# loop.run_until_complete(asyncio.wait(tasklist))
loop.run_until_complete(asyncio.gather(*tasklist))  # 与上面一样
# todo gather 比wait 更加高级
# gather 可以取消任务
print("time:", now() - start)
print(ListAll[-1])



del ListAll
ListAll1=[]

start = now()

def GenNum1(max):
     ListAll1.append([x for x in range(max)])

tasklist = [GenNum1(max) for max in range(1,11000)]
print("time:", now() - start)