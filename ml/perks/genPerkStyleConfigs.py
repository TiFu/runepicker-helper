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
    "columns": ["tag1", "tag2", "role", "root", "slow", "stun", "charm", "knockup", "heal", "shield",
        "base_ad", "base_health", "base_armor", "base_mres", "base_as", "ad_scaling", "health_scaling", 
        "armor_scaling", "mres_scaling", "as_scaling", "q_cd_early", "w_cd_early", "e_cd_early", "r_cd_early",
        "q_cd_late", "w_cd_late", "e_cd_late", "r_cd_late", "ap_ability_scaling_early", "ad_ability_scaling_early",
        "max_hp_scaling_early", "bonus_armor_scaling_early", "bonus_magic_resist_scaling_early",
        "ap_ability_scaling_late", "ad_ability_scaling_late",
        "max_hp_scaling_late", "bonus_armor_scaling_late", "bonus_magic_resist_scaling_late"],
    "predictColumn": "perk_primary_style",
    "nominalColumns": ["tag1", "tag2", "role", "perk_primary_style"],
    "trainDataPercentage": 0.9,
    "epochs": 30,
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
