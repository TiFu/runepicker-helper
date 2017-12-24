from aiohttp import web
import socketio
from runeproposer import RuneProposer
from models import Models
from config.config import config
from data import championById
import asyncio
from concurrent.futures import ThreadPoolExecutor
import constants

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
poolExecutor = ThreadPoolExecutor()
loop = asyncio.get_event_loop()

runeproposers = {}
models = Models(config["models"]["netConfigDir"], config["models"]["modelDir"],\
                     config["models"]["loss"], constants.styleNames)

def log(sid, event, data):
    print("[" + sid + "][" + event + "] " + data)

async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

# TODO: try catch for error reporting in case of crash
async def predictPrimaryStyle(sid, runeProposer, championId, lane):
    primaryStyles = runeProposer.predictPrimaryStyle(championId, lane)
    await sio.emit('primaryStyles', primaryStyles, namespace="/runeprediction", room=sid)

async def predictSubStyle(sid, runeProposer: RuneProposer):
    subStyles = runeProposer.predictSubStyle()
    await sio.emit("subStyles", subStyles, namespace="/runeprediction", room=sid)

async def predictPrimaryRunes(sid, runeProposer: RuneProposer):
    runes = runeProposer.predictPrimaryStyleRunes()
    await sio.emit("primaryRunes", runes, namespace="/runeprediction", room=sid)

async def predictSubRunes(sid, runePropsoer: RuneProposer):
    runes = runeProposer.predictSubStyleRunes()
    await sio.emit("subRunes", runes, namespace="/runeprediction", room=sid)

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
    runeproposers[sid] = RuneProposer();
    if not "champion_id" in data or not "lane" in data:
        return False, "Missing champion or lane!"
    if not data["champion_id"] in championById:
        return False, "Unknown Champion!"
    if data["lane"] not in constants.lanes:
        return False, "Unknown lane " + data["lane"] + ", expected " + str(constants.lanes)

    # Run prediction async to not block the whole event loop
    pred = loop.run_in_executor(poolExecutor, predictPrimaryStyle, sid, runeproposers[sid], data)  
    asyncio.ensure_future(pred)
    return True

@sio.on('selectPrimaryStyle', namespace='/runeprediction')
def selectPrimaryStyle(sid, data):
    log(sid, "selectPrimaryStyle", data)
    if data not in constants.styles:
        return False, "Invalid Style selected!"

    runeproposers[sid].selectPrimaryStyle(data)
    pred = loop.run_in_executor(poolExecutor, predictSubStyle, sid, runeproposers[sid])
    asyncio.ensure_future(pred)
    return True

@sio.on('selectSubStyle', namespace='/runeprediction')
def selectSubStyle(sid, data):
    print('disconnect ', sid)
    if data not in constants.styles:
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
    if not isinstance(data, list):
        return False, "List of 4 Runes is required!"
    if len(data) != 4:
        return False, "Please submit exactly 4 runes in the correct order"
    runesProposer = runeproposers[sid]
    for i in range(4):
        allowedRunes = constants.runesByPrimaryStyle[runeProposer.primaryStyle][i]
        if data[i] not in constants.runesByPrimaryStyle[runeProposer.primaryStyle][i]:
            return False, "Expected one of " + allowedRunes + ", but got " + data[i]
    
    runesProposer.selectPrimaryStyleRunes(data)
    pred = asyncio.run_in_executor(poolExecutor, predictSubRunes, sid, runeProposer)
    asyncio.ensure_future(pred)
    return True

@sio.on('disconnect', namespace='/runeprediction')
def disconnect(sid, data):
    log(sid, "disconnected", "")
    del runeproposers[sid]

app.router.add_static('/static', 'static')
app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app, host=config["websocket"]["host"], port=config["websocket"]["port"])