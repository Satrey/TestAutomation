import json
import socketio
import uvicorn
from fastapi import FastAPI

# Создаём экземпляр FastAPI приложения
app = FastAPI()

# Создаём экземпляр сервера Socket.IO с поддержкой асинхронного режима
sio = socketio.AsyncServer(async_mode='asgi')
# Оборачиваем FastAPI в Socket.IO ASGI приложение
socket_app = socketio.ASGIApp(sio, app)

users_list = {}

@sio.event
async def connect(sid, environ):
    print(f"Пользователь {sid} подключился")
    users_list[sid] = 0

@sio.event
async def disconnect(sid):
    print(f"Пользователь {sid} отключился")
    users_list.pop(sid)

@app.get("/")
async def get_index():
    for user in users_list.keys():
        print(f'Отпрака сообщения {user}')
        await sio.emit("message", {"text": "someone visited over http"}, to=user)
    return users_list

@app.post("/")
async def post_request(data):
    for user in users_list.keys():
        print(f'Отпрака сообщения на post запрос {user}')
        await sio.emit("message", {data}, to=user)


uvicorn.run(socket_app, host='0.0.0.0', port=8080)  