import asyncio


def callback(sleep_times):
    print("sleep {} success".format(sleep_times))


def stoploop(loop):
    loop.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    now = loop.time()
    # 都是异步方法，不会阻塞
    loop.call_later(2, callback, 2)  # 2秒后执行，   最后的2 是传递参数
    loop.call_later(1, callback, 1)
    loop.call_at(now + 2, callback, 3) # loop内部 时间加上2秒后执行

    loop.call_soon(callback, 4)
    # loop.call_soon(stoploop,loop)
    loop.run_forever()
