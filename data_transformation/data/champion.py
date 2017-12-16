import json

champion = json.load(open('data/champion.json'))

championById = {};

for champName in champion["data"]:
    data = champion["data"][champName];
    championById[data["key"]] = data;    
