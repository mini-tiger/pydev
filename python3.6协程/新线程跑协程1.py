from threading import Thread
import asyncio, time
def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def more_work(x):
    print('More work {}'.format(x))
    time.sleep(x)
    print('Finished more work {}'.format(x))

start = time.time()
new_loop = asyncio.new_event_loop()
t = Thread(target=start_loop, args=(new_loop,))  # 新线程 中跑协程,主线程不会阻塞， 新线程不会退出，所以会一直等待新任务执行
t.start()
print('TIME: {}'.format(time.time() - start))

for i in range(5):
	# new_loop.call_soon_threadsafe(more_work, 6)
	new_loop.call_soon_threadsafe(more_work, 1) # 新线程中会按照顺序执行call_soon_threadsafe方法注册的more_work方法, 没有并发
	print(i)
	time.sleep(1)

new_loop.stop()  # 这里不写这句 会一直阻塞主线程
