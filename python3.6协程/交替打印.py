import asyncio
import time

# now = lambda : time.time()
taskList = list()


async def do_some_work(x):
    # await asyncio.sleep(0) # 同步
    asyncio.sleep(0)
    # a.append(x)
    print('Waiting: ', x)


async def do_some_work1(x):
    # await asyncio.sleep(0)
    await asyncio.sleep(1) # 异步
    # a.append(x)
    print('Waiting: ', x)


# start = now()


loop = asyncio.get_event_loop()
# task = asyncio.ensure_future(coroutine)

# print(task)
# print (task._state)  # 运行前状态


# print(task)
# print(task._state)  # 运行后状态


for i in range(0, 10):
    if i % 2 == 0:
        taskList.append(asyncio.ensure_future(do_some_work(i)))
        # loop.run_until_complete(task)
    else:
        taskList.append(asyncio.ensure_future(do_some_work1(i)))

loop.run_until_complete(asyncio.gather(*taskList))

# print('TIME: ', now() - start)
