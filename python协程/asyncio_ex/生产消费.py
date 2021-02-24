import time
import asyncio
import queue
import threading
import uuid
import random
'''
基于协程的消费者模型，多个协程充当worker消费消息。
'''

now = lambda : time.time()

async def customer(num,q):
    print('任务 %d：start worker...' % num)
    while True:
        try:
            start = now()
            task = q.get(block=False)
            print('任务 %d：消费customer %s' % (num, task))
            await asyncio.sleep(10) # 假设每个消费者消费消息需要10秒，这样可以看出生产者生成的消息被不同的消费者消费
        except Exception as e:
            await asyncio.sleep(1)
            continue


async def run_async_customer(q):
    tasks = []
    for num in range(3):
        tasks.append(asyncio.create_task(customer(num,q)))
    await asyncio.gather(*tasks)

def product(q):
    print('product start...')
    while True:
        pro = '生产出产品 %s' % str(uuid.uuid1())
        print(pro)
        q.put(pro)
        time.sleep(random.randint(2,4))

def run(q):
    asyncio.run(run_async_customer(q))


if __name__ == '__main__':
    q = queue.Queue()
    # 开启一个线程运行生产者
    prod = threading.Thread(target=product, args=(q,))
    # 开启一个线程运行所有的消费者
    cust = threading.Thread(target=run, args=(q,))
    prod.start()
    cust.start()
    prod.join()
    cust.join()