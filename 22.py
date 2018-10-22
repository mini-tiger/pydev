import asyncio
import aiohttp

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def run():

    tasks = []
    for url in ["http://www.baidu.com","http://www.baidu.com"]:
        task = fetch(url)
        tasks.append(task)
        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        print(responses)


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
loop.close()