import json

config = {
    "layers": [
        {
            "type": "Dense",
            "activation": "tanh",
            "neuronCount": 200
        },
        {
            "type": "Dense",
            "activation": "tanh",
            "neuronCount": 50
        },
        {
            "type": "Dense",
            "activation": "tanh",
            "neuronCount": 200
        },
        {
            "type": "Dense",
            "activation": "tanh",
            "neuronCount": 30
        },
        {
            "type": "Dense",
            "activation": "softmax",
            "neuronCount": 5
        }
    ],
    "optimizer": "adam",
    "loss": "win_loss",
    "metrics": ["accuracy", "top_k_categorical_accuracy"],
    "top_k_parameter": 2,
    "oversample": True,
    "columns": ["champion_id", "tag1", "tag2", "role"],
    "predictColumn": "perk_primary_style",
    "nominalColumns": ["champion_id", "tag1", "tag2", "role", "perk_primary_style"],
    "trainDataPercentage": 0.9,
    "epochs": 15,
    "batchSize": 512
}

def makeConfigFile(outDir, name):
    for loss in ["win_loss", "categorical_crossentropy"]:
        config["loss"] = loss
        configFile = outDir + name + loss  + ".json"
        with open(configFile, 'w') as outfile:
            json.dump(config, outfile, indent=4)
            print("Created config " + str(configFile))

import os
outDir = "./netconfig/perkstyle/"
os.makedirs(outDir, exist_ok=True)
name = "primary_perkstyle_";

makeConfigFile(outDir, name)


config["columns"].append("perk_primary_style")
config["predictColumn"] = "perk_sub_style"
config["nominalColumns"].append("perk_sub_style")
name = "sub_perkstyle_"
makeConfigFile(outDir, name)

perkstyleMap = {
    8000: "precision",
    8100: "domination",
    8200: "sorcery",
    8300: "inspiration",
    8400: "resolve"
}

for perkstyle in [8000, 8100, 8200, 8300, 8400]:
    config["perkstyle_attribute"] = "perk_primary_style"
    layers = config["layers"]
    layers[len(layers) - 1]["neuronCount"] = 4
    name = "sub_perkstyle_" + perkstyleMap[perkstyle] + "_"
    config["perkstyle"] = perkstyle
    makeConfigFile(outDir, name)