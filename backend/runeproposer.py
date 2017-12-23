from abc import ABC
from typing import List
from .models import Models

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

class RuneProposer:

    def __init__(self, models: Models, preprocessing: DataPreprocessing):
        self.models = models
        sefl.preprocessing = preprocessing
 
    def predictPrimaryStyle(self, data): -> List[Option]
        pass
        
    def predictSubStyle(self, data): -> List[Option]
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