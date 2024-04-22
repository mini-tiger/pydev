from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse, ServerSentEvent
import asyncio
import uvicorn
app = FastAPI()


@app.get("/")
async def root(request: Request):
    async def event_generator(request: Request):
        res_str = "七夕情人节即将来临，我们为您准备了精美的鲜花和美味的蛋糕"
        for i in range(0,100000):
            if await request.is_disconnected():
                print("连接已中断")
                break
            yield {
                "event": "message",
                "retry": 15000,
                "data": i
            }

            await asyncio.sleep(0.2)

    g = event_generator(request)
    return EventSourceResponse(g,  ping=5,
        ping_message_factory=lambda: ServerSentEvent(**{"ping": 'connection test'}))

if __name__ == '__main__':
    uvicorn.run(app='生成目录:app', host="0.0.0.0", port=5000, reload=True)
