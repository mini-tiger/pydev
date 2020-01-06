import asyncio, time
from threading import Thread
def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

async def do_some_work(x):
    print('Waiting {}'.format(x))
    await asyncio.sleep(x)
    print('Done after {}s'.format(x))

# def more_work(x):
#     print('More work {}'.format(x))
#     time.sleep(x)
#     print('Finished more work {}'.format(x))

start = time.time()
new_loop = asyncio.new_event_loop()
t = Thread(target=start_loop, args=(new_loop,))
t.setDaemon(True) # 后台线程， 没找到 结束loop的方法，loop.stop不管用
t.start() # 不阻塞主线程， 主线程判断协程任务状态
print('TIME: {}'.format(time.time() - start))
tasks=[]
for i in range(5):
    task = asyncio.run_coroutine_threadsafe(do_some_work(1), new_loop) # 主线程通过run_coroutine_threadsafe新注册协程对象
    # asyncio.run_coroutine_threadsafe(do_some_work(4), new_loop)
    # print(i)
    # time.sleep(1)
    tasks.append(task)

# time.sleep(3)
# asyncio.gather(*asyncio.Task.all_tasks(),loop=new_loop).cancel()
for tt in tasks: # 这里判断协程状态
    while True:
        if tt._state == "FINISHED":
            break
# new_loop.stop()  # 这里不写这句 会一直阻塞主线程
# new_loop.close()
