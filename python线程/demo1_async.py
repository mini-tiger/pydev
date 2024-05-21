import asyncio
import random

class IPPool:
    def __init__(self, ip_list):
        self.ip_list = ip_list
        self.ip_queue = asyncio.Queue()
        for ip in self.ip_list:
            self.ip_queue.put_nowait(ip)

    async def acquire_ip(self):
        ip = await self.ip_queue.get()
        return ip

    async def release_ip(self, ip):
        await self.ip_queue.put(ip)

async def use_ip(ip_pool, thread_id):
    ip = await ip_pool.acquire_ip()
    print(f"Thread {thread_id} acquired IP: {ip}")
    s = random.randint(1, 5)
    await asyncio.sleep(s)  # 模拟使用IP的操作
    await ip_pool.release_ip(ip)
    print(f"Thread {thread_id} released IP: {ip}")
    return f"Thread {thread_id}, use ip: {ip}, sleep: {s} completed"

ip_list = ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4']
ip_pool = IPPool(ip_list)

async def main():
    tasks = [use_ip(ip_pool, i) for i in range(20)]
    results = await asyncio.gather(*tasks)
    return results

if __name__ == "__main__":
    result=asyncio.run(main())
    print(result)