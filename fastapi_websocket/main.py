import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict
from starlette.middleware.cors import CORSMiddleware
import base64
import os

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: int):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_personal_message(self, message: str, client_id: int):
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            await websocket.send_text(message)

    async def send_file(self, file_path: str, client_id: int):
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            with open(file_path, "rb") as file:
                encoded_file = base64.b64encode(file.read()).decode('utf-8')
                await websocket.send_text(encoded_file)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            if data.startswith("file:"):
                _, file_name, file_data = data.split(":", 2)
                decoded_data = base64.b64decode(file_data)
                with open(f"received_{file_name}", "wb") as file:
                    file.write(decoded_data)
                await manager.send_personal_message(f"File {file_name} received and saved.", client_id)
            else:
                await manager.send_personal_message(f"You sent: {data}", client_id)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast(f"Client #{client_id} left the chat")

if __name__ == "__main__":
    uvicorn.run(app='main:app', host="0.0.0.0", port=8002, reload=True)
