import asyncio
import time

now = lambda : time.time()

async def do_some_work(x):
    await asyncio.sleep(x)
    print('Waiting: ', x)

start = now()

coroutine = do_some_work(2)
loop = asyncio.get_event_loop()
# task = asyncio.ensure_future(coroutine)
task = loop.create_task(coroutine)
print(task)
print (task._state)  # 运行前状态

loop.run_until_complete(task)
print(task)
print(task._state)  # 运行后状态

print('TIME: ', now() - start)