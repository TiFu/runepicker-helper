from abc import ABC
from typing import List
from models import Models

class Option:
    def __init__(self, id: int, probability: float):
        self.id = id;
        self.probability = probability

class DataPreprocessing:
    
    def __init__(self, championJSONFile, wikiJSONFile):
        pass

    def preprocess(self, data):
        pass

# TODO: specify type for data
# Add validation for data
from constants import lanes, styles

class RuneProposer:

    def __init__(self, models: Models, preprocessing: DataPreprocessing):
        self.models = models
        self.preprocessing = preprocessing
        self.primaryStyle = -1
        self.subStyle = -1

    def isPrimaryStyleValid(self):
        return self.primaryStyle in styles

    def isSubStyleValid(self):
        return self.subStyle in styles and self.subStyle != self.primaryStyle

    def predictPrimaryStyle(self, championId, lane): -> List[Option]
        self.championId = championId
        self.lane = lane
        pass
        
    def predictSubStyle(self): -> List[Option]
        pass

    def predictPrimaryStyleRunes(self, data, primaryRuneStyle): -> List[int]
        pass

    def predictSubStyleRunes(self, data, subStyle): -> List[int]
        pass

    def selectPrimaryStyle(self, style: int):
        self.primaryStyle = style;

    def selectSubStyle(self, style: int):
        self.subStyle = style

# TODO: need more selects?