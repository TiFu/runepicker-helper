from aiohttp import web
import socketio
from runeproposer import RuneProposer
from models import Models
from config import config
from data import championById
import asyncio
from concurrent.futures import TaskPoolExecutor
import constants

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
poolExecutor = TaskPoolExecutor()
loop = asyncio.get_event_loop()

runeproposers = {}
models = new Models(config["models"]["netConfigDir"], config["models"]["modelDir"],\
                     config["models"]["loss"], constant.styleNames)

def log(sid, event, data):
    print("[" + sid + "][" + event + "] " + data)

async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

def predictPrimaryStyle(sid, runeProposer, championId, lane):
    primaryStyles = runeProposer.predictPrimaryStyle(championId, lane)
    await sio.emit('primaryStyles', primaryStyles, namespace="/runeprediction", room=sid)

def predictSubStyle(sid, runeProposer: RuneProposer):
    subStyles = runeProposer.predictSubStyle()
    await sio.emit("subStyles", subStyles, namespace="/runeprediction", room=sid)

def predictPrimaryRunes(sid, runeProposer: RuneProposer):
    runes = runeProposer.predictPrimaryStyleRunes()
    await sio.emit("primaryRunes", runes, namespace="/runeprediction", room=sid)

# TODO: implement logic here
@sio.on('connect', namespace='/runeprediction')
def connect(sid, environ):
    log(sid, "connect", "")

@sio.on('startPrediction', namespace='/runeprediction')
async def startPrediction(sid, data):
    """
        data:
            - champion id
            - lane
    """
    log(sid, "startPrediction", data)
    runeproposers[sid] = new RuneProposer();
    if not "champion_id" in data or not "lane" in data:
        return False, "Missing champion or lane!"
    if not data["champion_id"] in championById:
        return False, "Unknown Champion!"
    if data["lane"] not in lanes:
        return False, "Unknown lane " + data["lane"] + ", expected " + str(lanes)

    # Run prediction async to not block the whole event loop
    pred = loop.run_in_executor(poolExecutor, predictPrimaryStyle, sid, runeproposers[sid], data)  
    asyncio.ensure_future(pred)
    return True

@sio.on('selectPrimaryStyle', namespace='/runeprediction')
def selectPrimaryStyle(sid, data):
    log(sid, "selectPrimaryStyle", data)
    if data not in styles:
        return False, "Invalid Style selected!"

    runeproposers[sid].selectPrimaryStyle(data)
    pred = loop.run_in_executor(poolExecutor, predictSubStyle, sid, runeproposers[sid])
    asyncio.ensure_future(pred)
    return True

@sio.on('selectSubStyle', namespace='/runeprediction')
def selectSubStyle(sid, data):
    print('disconnect ', sid)
    if data not in styles:
        return False, "Invalid Style selected!"
    runeProposer = runeproposers[sid]
    if not runeProposer.isPrimaryStyleValid():
        return False, "Please select valid primary style first!"
    runeProposer.selectSubStyle(data)
    if not runeProposer.isSubStyleValid():
        runeProposer.selectSubStyle(-1)
        if runeProposer.subStyle == runeProposer.primaryStyle:
            return False, "Primary and sub style need to be different!"
        return False, "The selected substyle is invalid!"

    pred = asyncio.run_in_executor(poolExecutor, predictPrimaryRunes, sid, runeProposer)
    asyncio.ensure_future(pred)
    return True

@sio.on('selectPrimaryRunes', namespace='/runeprediction')
def selectPrimaryRunes(sid, data):
    # TODO: data validation lol => depends on input lel
    return False, "Not implemented"



@sio.on('selectSubRunes', namespace='/runeprediction')
def selectPrimaryRunes(sid, data):
    print('disconnect ', sid)
    return False, "Not implemented"

@sio.on('disconnect', namespace='/runeprediction')
def disconnect(sid, data):
    del runeproposers[sid]

app.router.add_static('/static', 'static')
app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app, host=config["host"], port=config["port"])