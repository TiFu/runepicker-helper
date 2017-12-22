import json

def loadNetConfig(file):
    netConfigDir = file.replace("perks/netconfig", "").replace(".json", "");
    print(netConfigDir)
    netConfig = json.load(open(file))
    netConfig["directory"] = netConfigDir
    return netConfig