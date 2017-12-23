from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

# TODO: implement logic here
@sio.on('connect', namespace='/runeprediction')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('startPrediction', namespace='/runeprediction')
async def startPrediction(sid, data):
    print("message ", data)
    await sio.emit('primaryStyles', "Hello " + data, namespace="/runeprediction", room=sid)

@sio.on('selectPrimaryStyle', namespace='/runeprediction')
def selectPrimaryStyle(sid, data):
    print('disconnect ', sid)

@sio.on('selectSubStyle', namespace='/runeprediction')
def selectSubStyle(sid, data):
    print('disconnect ', sid)
    # TODO: use callbacks (return) for error/success with asyncio.ensure_future

@sio.on('selectPrimaryRunes', namespace='/runeprediction')
def selectPrimaryRunes(sid, data):
    print('disconnect ', sid)

@sio.on('selectSubRunes', namespace='/runeprediction')
def selectPrimaryRunes(sid, data):
    print('disconnect ', sid)

app.router.add_static('/static', 'static')
app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app)