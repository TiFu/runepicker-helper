from abc import ABC
from typing import List
from models import Models

class Option:
    def __init__(self, id: int, probability: float):
        self.id = id;
        self.probability = probability

from data import championById, wikiById
import pandas as pd
import numpy as np

def getOrDefault(key, dict, default):
    if key in dict:
        return dict[key]
    else:
        return default

class DataPreprocessing:

    def getPrimaryPerks(self, primaryRunes):
        return primaryRunes[0], primaryRunes[1], primaryRunes[2], primaryRunes[3]

    def getSubPerks(self, subStyleRunes):
        if subStyleRunes is not None:
            if substyleRunes[0] > substyleRunes[1]:
                perk4 = substyleRunes[1]
                perk5 = substyleRunes[0]
            else:
                perk4 = substyleRunes[0]
                perk5 = substyleRunes[1]
        else:
            perk4 = -1
            perk5 = -1  
        return (perk4, perk5)

    def getTags(self, championId):
        tags = championById[championId]["tags"]
        tag1 = tags[0]
        tag2 = "NULL"
        if len(tags) > 1:
            tag2 = tags[1]
        return tag1, tag2

    def getCC(self, wiki):
        slow = getOrDefault("slow", wiki["keywords"], 0)
        root = getOrDefault("root", wiki["keywords"], 0)
        stun = getOrDefault("stun", wiki["keywords"], 0)
        charm = getOrDefault("charm", wiki["keywords"], 0)
        knockup = getOrDefault("knockup", wiki["keywords"], 0)
        heal = getOrDefault("heal", wiki["keywords"], 0)
        shield = getOrDefault("shield", wiki["keywords"], 0)
        return slow, root, stun, charm, knockup, heal, shield

    def getCooldown(self, wiki, time):
        cd = wiki[time]["cooldown"]
        qCd = getOrDefault("skill_q", cd, 0)
        wCd = getOrDefault("skill_w", cd, 0)
        eCd = getOrDefault("skill_e", cd, 0)
        rCd = getOrDefault("skill_r", cd, 0)   
        return qCd, wCd, eCd, rCd     

    def setPrimaryStle(self, data, primaryStyle):
        data[0, "perk_primary_style"] = primaryStyle
        return data

    def setSubStyle(self, data, subStyle):
        data[0, "perk_sub_style"] = subStyle
        return data
    
    def setPrimaryStyleRunes(self, data, primaryStyleRunes):
        for i in range(len(primaryStyleRunes)):
            data[0, "perk" + str(i)] = primaryStyleRunes[i]
        return data
        
    def setSubStyleRunes(self, data, subStyleRunes):
        for i in range(len(subStyleRunes)):
            data[0, "perk" + str(4 + i)] = subStyleRunes[i]
        return data

    # TODO: this can be done more cleanly with a couple loops i.e. 
    # iterate over stats and append to data
    def preprocess(self, championId, role, primaryStyle, subStyle, primaryStyleRunes, subStyleRunes):
        champion = championById[championId]
        wiki = wikiById[championId]

        tag1, tag2 = self.getTags(championId)
        perk0, perk1, perk2, perk3, perk4 = self.getPrimaryPerks(primaryStyleRunes)
        perk4, perk5 = self.getSubPerks(subStyleRunes)
 
        resources = getOrDefault("partype", champion, "None");
        slow, root, stun, charm, knockup, heal, shield = self.getCC(wiki)
        
        # champ stats
        stats = champion["stats"]
        hp = stats["hp"]
        hpScaling = stats["hpperlevel"]
        armor = stats["armor"]
        armorScaling = stats["armorperlevel"]
        ad = stats["attackdamage"]
        adScaling = stats["attackdamageperlevel"]
        mres = stats["spellblock"]
        mresScaling = stats["spellblockperlevel"]
        asOffset = stats["attackspeedoffset"]
        asScaling = stats["attackspeedperlevel"]
 
        # Cooldowns
        qCdEarly, wCdEarly, eCdEarly, rCdEarly = self.getCooldown(wiki, "early")
        qCdLate, wCdLate, eCdLate, rCdLate = self.getCooldown(wiki, "late")

        # Ability scalings
        early = wiki["early"]
        late = wiki["late"]
        ap_ability_scaling_early = getOrDefault("AP", early, 0)
        ad_ability_scaling_early = getOrDefault("AD", early, 0) 
        max_hp_scaling_early = getOrDefault("maximum health", early, 0)
        bonus_armor_scaling_early = getOrDefault("bonus armor", early, 0)
        bonus_magic_resist_scaling_early = getOrDefault("bonus magic resistance", early, 0)
        
        ap_ability_scaling_late = getOrDefault("AP", late, 0)
        ad_ability_scaling_late = getOrDefault("AD", late, 0) 
        max_hp_scaling_late = getOrDefault("maximum health", late, 0)
        bonus_armor_scaling_late = getOrDefault("bonus armor", late, 0)
        bonus_magic_resist_scaling_late = getOrDefault("bonus magic resistance", late, 0)

        data = np.array([
            championId, tag1, tag2, role, root, slow,
            stun, charm, knockup, heal, shield, base_ad, 
            base_health, base_armor, base_mres, base_as,
            ad, health, armor, mres, asOffset, 
            asScaling, qCdEarly, wCdEarly, eCdEarly, 
            rCdEarly, qCdLate, wCdLate, eCdLate, 
            rCdLate, ap_ability_scaling_early, ad_ability_scaling_early,
            max_hp_scaling_early, bonus_armor_scaling_early, 
            bonus_magic_resist_scaling_early, ap_ability_scaling_late,
            ad_ability_scaling_late, max_hp_scaling_late, 
            bonus_armor_scaling_late, bonus_magic_resist_scaling_late,
            resources, primaryStyle, subStyle,
            perk0, perk1, perk2, perk3, perk4, perk5, 1
        ])
        columns = ["champion_id", "tag1", "tag2", "role", "root", "slow", \
                    "stun", "charm", "knockup", "heal", "shield", "base_ad", \
                    "base_health", "base_armor", "base_mres", "base_as", \
                    "ad_scaling", "health_scaling", "armor_scaling", "mres_scaling", \
                    "as_scaling", "q_cd_early", "w_cd_early", "e_cd_early", \
                    "r_cd_early", "q_cd_late", "w_cd_late", "e_cd_late", \
                    "r_cd_late", "ap_ability_scaling_early", "ad_ability_scaling_early", \
                    "max_hp_scaling_early", "bonus_armor_scaling_early", \
                    "bonus_magic_resist_scaling_early", "ap_ability_scaling_late", \
                    "ad_ability_scaling_late", "max_hp_scaling_late", \
                    "bonus_armor_scaling_late", "bonus_magic_resist_scaling_late", \
                    "resource", "perk_primary_style", "perk_sub_style", \
                    "perk0", "perk1", "perk2", "perk3", "perk4", "perk5", "win"]
        # now put this into a df lol
        df = pd.DataFrame(data, columns=columns)
        return df

from constants import lanes, styles

class RuneProposer:

    def __init__(self, models: Models, preprocessing: DataPreprocessing):
        self.models = models
        self.preprocessing = preprocessing
        self.primaryStyle = -1
        self.subStyle = -1
        self.primaryRunes = []
        self.subRunes = []
        self.championId = None
        self.lane = None
        self.data = None

    def isPrimaryStyleValid(self):
        return self.primaryStyle in styles

    def isSubStyleValid(self):
        return self.subStyle in styles and self.subStyle != self.primaryStyle

    def predictPrimaryStyle(self, championId, lane): -> List[Option]
        self.championId = championId
        self.lane = lane
        self.data = self.preprocessing.preprocess(championId, lane, 0, 0, None, None)
        model = self.models.getPrimaryStyleModel();
        return model.predict(self.data)
    
    def predictSubStyle(self): -> List[Option]
        model = self.models.getSubStyleModel()
        prediction = model.predict(self.data)
        return prediction

    def predictPrimaryStyleRunes(self): -> List[int]
        predictions = []
        for perk in [0,1,2,3]:
            model = self.models.getPrimaryStyleRunesModel(self.primaryStyle, perk)
            prediction = model.predict(self.data)
            predictions.append(prediction)
        return predictions

    def predictSubStyleRunes(self, data, subStyle): -> List[int]
        predictions = []
        for perk in [4,5]:
            model = self.models.getSubStyleRunesModel(self.subStyle, perk)
            prediction = model.predict(self.data)
            predictions.append(prediction)
        return predictions

    def selectPrimaryStyleRunes(self, runes):
        self.primaryRunes = runes
        self.data = self.preprocessing.setPrimaryStyleRunes(self.data, runes)

    def selectSubStyleRunes(self, runes):
        self.subRunes = runes
        self.data = self.preprocessing.setSubStyleRunes(self.data, runes)

    def selectPrimaryStyle(self, style: int):
        self.primaryStyle = style;
        self.data = self.preprocessing.setPrimaryStyle(self.data, style)

    def selectSubStyle(self, style: int):
        self.subStyle = style
        self.data = self.preprocessing.setSubStyle(self.data, style)
