from threading import Thread
import asyncio, time

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def y(filename):
    with open(filename,"rb") as f:
        ff = await f.readlines()
    # await asyncio.sleep(1)
    # return ff

async def do_some_work(x):
    print('Waiting {}'.format(x))
    await y("c:\\get-pip.py") # 将读取文件放到 协程中，异步
    # print(f)
    # await asyncio.sleep(3)
    print('Done after {}s'.format(x))

# def more_work(x):
#     print('More work {}'.format(x))
#     time.sleep(x)
#     print('Finished more work {}'.format(x))

start = time.time()
new_loop = asyncio.new_event_loop()
t = Thread(target=start_loop, args=(new_loop,))
t.setDaemon(True)
t.start()
print('TIME: {}'.format(time.time() - start))



try:
    tasks=[]
    for i in range(30):
        task = asyncio.run_coroutine_threadsafe(do_some_work(i), new_loop)
        tasks.append(task)
    # asyncio.run_coroutine_threadsafe(do_some_work(1), new_loop)

finally:
    # print(asyncio.Task.all_tasks(loop=new_loop))
    for tt in tasks:  # 这里判断协程状态
        while True:
            if tt._state == "FINISHED":
                break
    # for tt in tasks:
    #     asyncio.wait(fs=tt, loop=new_loop)
    #     asyncio.as_completed(fs=tt, loop=new_loop)
    # new_loop.stop()
    # new_loop.close()
# new_loop.stop()