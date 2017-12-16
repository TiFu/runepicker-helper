import json
from .champion import champion

wiki = json.load(open('data/wiki.json'))

mappedNames = set([
    "MasterYi",
    "KogMaw",
    "XinZhao",
    "Wukong",
    "RekSai",
    "AurelionSol",
    "TahmKench",
    "MissFortune",
    "LeeSin",
    "JarvanIV",
    "TwistedFate",
    "DrMundo"
])

def map(champName):
    champName = champName.replace(".", "")
    if champName == "Wukong":
        return "MonkeyKing"
    if champName in mappedNames:
        return champName
    return champName.capitalize()

wikiById = {}
for champName in wiki["scaling"]:
    mappedChampName = map(champName)
    data = champion["data"][mappedChampName];
    wikiById[data["key"]] = wiki["scaling"][champName];    