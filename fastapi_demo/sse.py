from fastapi import FastAPI, Request, Response
from starlette.responses import StreamingResponse
import asyncio
import uvicorn,json

app = FastAPI()
async def generate_events111():
    for i in range(10):
        # 直接生成数据，这里用 f-string 模拟数据
        data1 = f"Data from source 111, event {i}"

        # 生成 SSE 格式的数据
        yield f"data: {data1}\n\n"

        await asyncio.sleep(1)  # 模拟间隔时间

def event_stream111():
    return generate_events111()

@app.get("/event111", response_class=StreamingResponse)
async def event111(request: Request):
    response = StreamingResponse(event_stream111(), media_type="text/event-stream")
    return response

async def get_data_from_source1():
    # 模拟从数据源1异步获取数据
    await asyncio.sleep(1)
    return "Data from source 1"

async def get_data_from_source2():
    # 模拟从数据源2异步获取数据
    await asyncio.sleep(2)
    return "Data from source 2"

def process_data(data1, data2):
    # 处理数据
    return f"Processed {data1} and {data2}"

async def event_stream_processor():
    while True:
        # 并发获取数据
        data1, data2 = await asyncio.gather(
            get_data_from_source1(),
            get_data_from_source2()
        )

        # 处理数据
        result = process_data(data1, data2)

        # 生成SSE格式的数据
        yield f"data: {result}\n\n"
        await asyncio.sleep(1)  # 模拟间隔时间

def event_stream():
    return event_stream_processor()

@app.get("/events", response_class=StreamingResponse)
async def events(request: Request):
    response = StreamingResponse(event_stream(), media_type="text/event-stream")
    return response


async def get_data_from_source3():
    i = 0
    while i < 5:
        await asyncio.sleep(2)  # 模拟延迟
        i += 1
        yield f"Data from source {i}"

async def get_data_from_source4():
    while True:
        await asyncio.sleep(1)  # 模拟延迟
        yield "Data from source 4"

async def event_stream_processor1():
    generator3 = get_data_from_source3()  # 创建get_data_from_source3的生成器实例
    generator4 = get_data_from_source4()  # 创建get_data_from_source4的生成器实例
    task3 = asyncio.create_task(generator3.__anext__())
    task4 = asyncio.create_task(generator4.__anext__())
    while True:
        done, pending = await asyncio.wait([task3, task4], return_when=asyncio.FIRST_COMPLETED)
        if task3 in done:
            data = task3.result()
            yield f"data: {data}\n\n"
            if not data.startswith("Data from source 5"):  # 确保数据源3不超出范围
                task3 = asyncio.create_task(generator3.__anext__())
        if task4 in done:
            data = task4.result()
            yield f"data: {data}\n\n"
            task4 = asyncio.create_task(generator4.__anext__())

def event_stream1():
    return event_stream_processor1()

@app.get("/events1", response_class=StreamingResponse)
async def events1(request: Request):
    response = StreamingResponse(event_stream1(), media_type="text/event-stream")
    return response


import time
async def get_data_from_source5():
    i = 0
    while i < 5:
        await asyncio.sleep(2)  # 使用异步方式模拟延迟
        i += 1
        yield f"Data from source {i}"

async def get_data_from_source6():
    while True:
        await asyncio.sleep(1)  # 使用异步方式模拟延迟
        yield "Data from source 6"

async def event_stream_processor2():
    task5 = asyncio.ensure_future(get_data_from_source5().__anext__())
    task6 = asyncio.ensure_future(get_data_from_source6().__anext__())
    while True:
        done, pending = await asyncio.wait([task5, task6], return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            try:
                data = task.result()
                yield f"data: {data}\n\n"
                if task == task5:
                    task5 = asyncio.ensure_future(get_data_from_source5().__anext__())
                elif task == task6:
                    task6 = asyncio.ensure_future(get_data_from_source6().__anext__())
            except StopAsyncIteration:
                pass

def event_stream2():
    return event_stream_processor2()
@app.get("/events2", response_class=StreamingResponse)
async def events2(request: Request):
    response = StreamingResponse(event_stream2(), media_type="text/event-stream")
    return response

if __name__ == "__main__":
    uvicorn.run(app='sse:app', host="0.0.0.0", port=8012, reload=True)
