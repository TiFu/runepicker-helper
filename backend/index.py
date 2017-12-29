from aiohttp import web
import socketio
from runeproposer import RuneProposer, DataPreprocessing
from models import Models
from config.config import config
from data import championById
import asyncio
from concurrent.futures import ThreadPoolExecutor
import constants
import traceback

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
poolExecutor = ThreadPoolExecutor()
loop = asyncio.get_event_loop()

runeproposers = {}
models = Models(config["models"]["netConfigDir"], config["models"]["modelDir"],\
                     config["models"]["loss"], constants.styleNames)

preprocessing = DataPreprocessing()

def log(sid, event, data):
    print("[" + sid + "][" + event + "] " + str(data))

async def index(request):
    """Serve the client-side application."""
    with open('static/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

def emit(sid, evt, success, data):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    emit = sio.emit(evt, { "success": success, "data": data}, namespace="/runeprediction", room=sid)
    loop.run_until_complete(emit)

# TODO: try catch for error reporting in case of crash
def predictPrimaryStyle(sid, runeProposer, championId, lane):
    try:
        log(sid, "predictPrimaryStyle", "Starting prediction")
        primaryStyles = runeProposer.predictPrimaryStyle(championId, lane)
        log(sid, "predictPrimaryStyle", "predicted runes: "  + str(primaryStyles))
        emit(sid, 'primaryStyles', True, primaryStyles)
        log(sid, "predictPrimaryStyle", "Send response!")
    except Exception as err:
        emit(sid, 'primaryStyles', False, "Something went wrong!")
        tb = traceback.format_exc()
        log(sid, "predictPrimartyStyle", err)
        print(tb)

def predictSubStyle(sid, runeProposer: RuneProposer):
    try:
        subStyles = runeProposer.predictSubStyle()
        emit(sid, "subStyles", True, subStyles)
    except Exception as err:
        emit(sid, "subStyles", False, "Something went wrong!")
        log(sid, "predictSubStyle", err)
        tb = traceback.format_exc()
        print(tb)

def predictPrimaryRunes(sid, runeProposer: RuneProposer):
    try:
        runes = runeProposer.predictPrimaryStyleRunes()
        emit(sid, "primaryRunes", True, runes)
    except Exception as err:
        emit(sid, "primaryRunes", False, "Something went wrong!")
        log(sid, "predictPrimaryRunes", err)
        tb = traceback.format_exc()
        print(tb)

def predictSubRunes(sid, runeProposer: RuneProposer):
    try:
        log(sid, "predictSubRunes", "predicting sub runes")
        runes = runeProposer.predictSubStyleRunes()
        log(sid, "predictSubRunes", "predicted sub runes")
        emit(sid, "subRunes", True, runes)
    except Exception as err:
        emit(sid, "subRunes", False, "Something went wrong!")
        log(sid, "predictSubRunes", err)
        tb = traceback.format_exc()
        print(tb)

@sio.on('connect', namespace='/runeprediction')
def connect(sid, environ):
    log(sid, "connect", "")

@sio.on('startPrediction', namespace='/runeprediction')
async def startPrediction(sid, data):
    """
        data: dict of
            - champion id
            - lane
    """
    log(sid, "startPrediction", data)
    runeproposers[sid] = RuneProposer(models, preprocessing);
    if not "champion_id" in data or not "lane" in data:
        return False, "Missing champion or lane!"
    data["champion_id"] = str(data["champion_id"])
    if not data["champion_id"] in championById:
        return False, "Unknown Champion!"
    if data["lane"] not in constants.lanes:
        return False, "Unknown lane " + data["lane"] + ", expected " + str(constants.lanes)

    # Run prediction async to not block the whole event loop
    pred = loop.run_in_executor(poolExecutor, predictPrimaryStyle, sid, runeproposers[sid], data["champion_id"], data["lane"])
    asyncio.ensure_future(pred)
    return True

@sio.on('selectPrimaryStyle', namespace='/runeprediction')
def selectPrimaryStyle(sid, data):
    log(sid, "selectPrimaryStyle", data)
    if data not in constants.styles:
        return False, "Invalid Style selected!"

    runeproposers[sid].selectPrimaryStyle(data)
    pred = loop.run_in_executor(poolExecutor, predictPrimaryRunes, sid, runeproposers[sid])
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

    pred = loop.run_in_executor(poolExecutor, predictSubRunes, sid, runeProposer)
    asyncio.ensure_future(pred)
    return True

@sio.on('selectPrimaryRunes', namespace='/runeprediction')
def selectPrimaryRunes(sid, data):
    if not isinstance(data, list):
        return False, "List of 4 Runes is required!"
    if len(data) != 4:
        return False, "Please submit exactly 4 runes in the correct order"
    runeProposer = runeproposers[sid]
    for i in range(4):
        allowedRunes = constants.runesByPrimaryStyle[runeProposer.primaryStyle][i]
        if data[i] not in constants.runesByPrimaryStyle[runeProposer.primaryStyle][i]:
            return False, "Expected one of " + allowedRunes + ", but got " + data[i]
    print("Select primary style runes: " + str(data))
    runeProposer.selectPrimaryStyleRunes(data)
    print("Selected primary style runes: " + str(data))
    pred = loop.run_in_executor(poolExecutor, predictSubStyle, sid, runeProposer)
    asyncio.ensure_future(pred)
    return True

@sio.on('disconnect', namespace='/runeprediction')
def disconnect(sid):
    log(sid, "disconnected", "")
    del runeproposers[sid]

app.router.add_static('/static', 'static')
app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app, host=config["websocket"]["host"], port=config["websocket"]["port"])
