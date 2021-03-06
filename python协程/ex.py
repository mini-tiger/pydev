import asyncio

import time

now = lambda: time.time()

async def do_some_work(x):
    print('等待 %s 秒 ' %(x))

    await asyncio.sleep(x) # 模拟阻塞， 协程的控制权让出，以便loop调用其他的协程
    return 'Done after {}s'.format(x)

start = now()

# coroutine1 = do_some_work(1)
# coroutine2 = do_some_work(2)
# coroutine3 = do_some_work(4)


a=asyncio.ensure_future(do_some_work(1))
b=asyncio.ensure_future(do_some_work(2))
    # coroutine3


loop = asyncio.get_event_loop() #　创建LOOP主线程，所有协程都在这个线程中
# loop.run_until_complete(asyncio.wait(tasks)) #  开始运行 run_until_complete直到都运行完,asyncio.wait 接受列表，

loop.run_until_complete(asyncio.gather(*[a,b])) # asyncio.wait 接受很多task
print(a,a.result())
print(b,b.result())
# result = (asyncio.gather(*tasks) 返回列表，result每项是 协程对象return回来的结果，推荐



print("=="*50)
# asyncio.wait() 返回set(), 通过a=create_task() 获取结果 frist.py
result,ok =loop.run_until_complete(asyncio.wait([a,b]))
print(result)
print(ok)


print('TIME: ', now() - start)
