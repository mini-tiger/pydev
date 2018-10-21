import asyncio

import time

now = lambda: time.time()

async def do_some_work(x):
    print('等待 %s 秒 ' %(x))

    await asyncio.sleep(x) # 模拟阻塞， 协程的控制权让出，以便loop调用其他的协程
    return 'Done after {}s'.format(x)

start = now()

coroutine1 = do_some_work(1)
coroutine2 = do_some_work(2)
coroutine3 = do_some_work(4)

tasks = [
    asyncio.ensure_future(coroutine1),
    asyncio.ensure_future(coroutine2),
    asyncio.ensure_future(coroutine3)
]

loop = asyncio.get_event_loop() #　创建LOOP主线程，所有协程都在这个线程中
# loop.run_until_complete(asyncio.wait(tasks)) #  开始运行 run_until_complete直到都运行完,asyncio.wait 接受列表，

loop.run_until_complete(asyncio.gather(*tasks)) # asyncio.wait 接受很多task

# while True:
# 	for task in asyncio.Task.all_tasks():
# 		if task._state == "FINISHED":
# 			break
# 	break

for task in tasks:
    print('Task ret: ', task.result())

print('TIME: ', now() - start)
