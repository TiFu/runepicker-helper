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
            "neuronCount": 8
        }
    ],
    "optimizer": "adam",
    "loss": "win_loss",
    "oversample": True,
    "metrics": ["accuracy", "top_k_categorical_accuracy"],
    "top_k_parameter": 2,
    "columns": ["tag1", "tag2", "role", "root", "slow", "stun", "charm", "knockup", "heal", "shield",
        "base_ad", "base_health", "base_armor", "base_mres", "base_as", "ad_scaling", "health_scaling", 
        "armor_scaling", "mres_scaling", "as_scaling", "q_cd_early", "w_cd_early", "e_cd_early", "r_cd_early",
        "q_cd_late", "w_cd_late", "e_cd_late", "r_cd_late", "ap_ability_scaling_early", "ad_ability_scaling_early",
        "max_hp_scaling_early", "bonus_armor_scaling_early", "bonus_magic_resist_scaling_early",
        "ap_ability_scaling_late", "ad_ability_scaling_late",
        "max_hp_scaling_late", "bonus_armor_scaling_late", "bonus_magic_resist_scaling_late"],
    "predictColumn": "perk4",
    "nominalColumns": ["tag1", "tag2", "role", "perk4"],
    "perkstyle": 8000,
    "perkstyle_attribute": "perk_sub_style",
    "trainDataPercentage": 0.9,
    "epochs": 30,
    "batchSize": 512,
    "modelName": "primary_perkstyle/precision"
}

def makeConfigFile(outDir, perks, outputDim, style_attribute):
    config["layers"][len(config["layers"]) - 1]["neuronCount"] = outputDim
    for perkstyle in [8000, 8100, 8200, 8300, 8400]:
        config["perkstyle"] = perkstyle
        config["perkstyle_attribute"] = style_attribute
        os.makedirs(outDir + perkstyleMap[perkstyle], exist_ok=True)
        for perk in perks:
            config["predictColumn"] = perk
            # assume that the last item in nominal colmuns is what we prdict
            config["nominalColumns"][len(config["nominalColumns"]) - 1] = perk
            for loss in ["win_loss", "categorical_crossentropy"]:
                config["loss"] = loss
                configFile = outDir + perkstyleMap[perkstyle] + "/" + perk + "_" + loss  + ".json"
                with open(configFile, 'w') as outfile:
                    json.dump(config, outfile, indent=4)
                    print("Created config " + str(configFile))

perkstyleMap = {
    8000: "precision",
    8100: "domination",
    8200: "sorcery",
    8300: "inspiration",
    8400: "resolve"
}
import os
outDir = "./netconfig/perks/primary/"
os.makedirs(outDir, exist_ok=True)
makeConfigFile(outDir, ["perk0", "perk1", "perk2", "perk3"], 3, "perk_primary_style")

outDir = "./netconfig/perks/secondary/"
os.makedirs(outDir, exist_ok=True)
makeConfigFile(outDir, ["perk4", "perk5"], 8, "perk_sub_style")