import asyncio
import functools
from asyncio import Lock


def unlock(lock):
    print('callback releasing lock')
    lock.release()


async def coro1(lock):
    print('coro1 wating for the lock')
    with await lock:
        print('coro1 acquired lock')
    print('coro1 released lock')


async def coro2(lock):
    print('coro2 wating for the lock')
    await lock
    try:
        print('coro2 acquired lock')
    finally:
        print('coro2 released lock')
        lock.release()


async def main(loop):
    lock = Lock()
    print('协程开始前，先锁住')
    await lock.acquire()
    print('是否有锁: {}'.format(lock.locked()))

    loop.call_later(0.1, functools.partial(unlock, lock)) # 0.1秒后执行 unlock(lock)，解锁

    print('等待执行协程') #
    await asyncio.wait([coro1(lock), coro2(lock)])


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()