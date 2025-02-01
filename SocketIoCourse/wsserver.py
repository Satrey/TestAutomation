import time

import socketio
from flask import Flask

users_list = []
counter = 0
users_counters = {}

# Создаем сервер Socket.IO
sio = socketio.Server(cors_allowed_origins=
                      {
                          "192.168.1.30",
                          "192.168.1.20",
                          "*"
                      }
)

# Создаем приложение Flask
app = Flask(__name__)

# Подключаем сервер Socket.IO к Flask
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)


# Обработчики событий Socket.IO
@sio.event
def connect(sid, environ):
    print(f"Клиент {sid} подключился")
    users_counters[sid] = 0
    time.sleep(2)
    sio.emit("message", {"msg": "hello message!"}, to=sid)
    print('Список пользователей - ', users_counters)


@sio.event
def disconnect(sid):
    users_counters.pop(sid)
    print(f"Клиент {sid} отключился")
    print('Список пользователей - ', users_counters)

@sio.event
def welcome(sid, data):
    sio.emit("welcome", {"msg": f"Welcome event{data}"}, to=sid)

@sio.event
def message(sid, data):
    print(f"Сообщение от {sid}: {data}")
    sio.emit("message", {"msg": f"Эхо: {data}"}, to=sid)

@sio.event
def join(sid, data):
    sio.emit("status_update", {"msg": f"Эхо: {data}"}, to=sid)

@sio.event
def get_users_online(sid, environ):
    sio.emit("users", {"online": len(users_list)}, to=sid)
    print(f'Количество пользователей онлайн - {len(users_list)}')

@sio.event
def count_queries(sid, environ):
    sio.emit("users", {"counter": counter}, to=sid)
    print(f'Количество запросов - {counter}')

@sio.event
def increase(sid, environ):
    users_counters[sid] += 1
    print('Счетчик увеличен на еденицу - ', users_counters.values())
    print(users_counters)

@sio.event
def decrease(sid, environ):
    if users_counters[sid] > 0:
        users_counters[sid] -= 1
        print('Счетчик увеличен на еденицу - ', users_counters.values())
    else:
        print('Счетчик пользователя равен нулю! ', users_counters[sid])
    print(users_counters)

@sio.on('*')
def catch_all(event, sid, data):
    global counter
    sio.emit("error", {"message": f"No handler for event {event}"})   
    counter += 1
    print(counter)


# Запуск приложения
if __name__ == "__main__":
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)