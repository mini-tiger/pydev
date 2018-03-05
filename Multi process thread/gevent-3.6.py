import threading
import asyncio,time

# @asyncio.coroutine
# def hello():
#     print('Hello world! (%s)' % threading.currentThread())
#     yield from asyncio.sleep(1)
#     print('Hello again! (%s)' % threading.currentThread())

# print (dir(asyncio))
t=time.time()

# @asyncio.coroutine
# def func(i):
# 	tt=(t)
# 	s=0
# 	yield from asyncio.sleep(0)
# 	while i > 0:
# 		s=s+i
# 		i=i-1
# 	print (s)
# 	print (time.time()-tt)
async def summ(i):
	s=0
	while i > 0:
		s=s+i
		i=i-1
	return s


async def func(i):
	tt=(t)
	s=await summ(i)
	print (s)
	print (time.time()-tt)

loop = asyncio.get_event_loop()
tasks = [func(20000000),func(20000000)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

