import asyncio
import threading

from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


async def async_generator():
    for i in range(10):
        yield 'data: %d\n\n' % i
        await asyncio.sleep(1)


@app.route('/')
def index():
    return render_template('flask_socketio_client.html')


@socketio.on('start')
def handle_start():
    def run_loop(target_loop):
        asyncio.set_event_loop(target_loop)
        target_loop.run_until_complete(async_emit())

    async def async_emit():
        async for data in async_generator():
            socketio.emit('response', {'data': data})

    loop = asyncio.new_event_loop()
    t = threading.Thread(target=run_loop, args=(loop,))
    t.start()


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
