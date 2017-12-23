from keras.models import load_model
import json
import os.path as path
from typing import List, Mapping
import keras.backend as K
import keras.metrics as metrics
import pickle
from get_smarties import Smarties

def makeTopKAccuracy(k):
    def topKAccuracy(y_true, y_pred): 
        return metrics.top_k_categorical_accuracy(y_true, y_pred, k)
    return topKAccuracy

def maskedErrorFunc(y_true, y_pred):
    mask = K.cast(K.not_equal(y_true, -1), K.floatx())
    maskedError = (y_true - y_pred) * mask
    correct = K.mean(K.square(maskedError))
    return correct

# netConfigName is path from netConfig dir (RELATIVE to netConfig Dir) to the json file
class Model:
    def __init__(self, netConfigsDir, modelDir, netConfigName):
        self.netConfig = self._loadNetConfig(netConfigsDir, netConfigName)
        self.topKAccuracy = makeTopKAccuracy(self.netConfig["top_k_parameter"])
        self.smarties = self._loadSmarties(modelDir, self._getModelName())
        self.model = self.loadModel(modelDir, self._getModelName())

    def _loadSmarties(self, modelDir, modelFile):
        smartiesFile = path.join(modelDir, modelFile, "smarties.pkl")
        with open(smartiesFile, "rb") as smarties:
            return pickle.load(smarties)
    
    def _getModelName(self):
        return self.netConfig["directory"]
    
    def _loadNetConfig(self, netConfigsDir, netConfigName):
        netConfig = json.load(open(path.join(netConfigsDir, netConfigName)))
        netConfig["directory"] = netConfigName.replace(".json", "")
        return netConfig

    def loadModel(self, modelDir, modelFile):
        modelFile = path.join(modelDir, modelFile, "model");
        return load_model(modelFile, custom_objects={"topKAccuracy": self.topKAccuracy, "win_loss": maskedErrorFunc})

    # TODO: decide on data structure
    def predict(self, fullData):
        # TODO: select columns, apply smarties, predict and return with column names or so
        # needs copy of neural net code
        pass

    def _selectSubsetData(self, fullData):
        pass

class Models:
    
    def __init__(self, netConfigDir, modelDir, lossFunction, styleNames: Mapping[int, str] ):
        self.netConfigDir = netConfigDir
        self.modelDir = modelDir
        self.lossFunction = lossFunction
        self.styleModels = {}
        self.perkModels = {}
        self.styleNames = styleNames

    def getPrimaryStyleModel(self)-> Model:
        return self._getStyleModel("primary");

    def getSubStyleModel(self)-> Model:
        return self._getStyleModel("sub");

    def getPrimaryStyleRunesModel(self, primaryStyle: int, perk: int)-> Model:
        return self._getPerkModel("primary", primaryStyle, perk);

    def getSubStyleRunesModel(self, subStyle: int, perk: int)-> Model:
        return self._getPerkModel("secondary", subStyle, perk);

    def _getPerkModel(self, styleType: str, style: int, perk: int)-> Model:
        if styleType not in self.perkModels:
            self.perkModels[styleType] = {}
        if str(style) not in self.perkModels:
            self.perkModels[str(style)] = {}
        if str(perk) not in self.perkModels[str(style)]:
            modelName = self._getPerkModelName(styleType, style, perk)
            self.perkModels = Model(self.netConfigDir, self.modelDir, modelName)
        return self.perkModels[str(style)][str(perk)]

    def _getPerkModelName(self, styleType: str, style: int, perk: int)-> str:
        return path.join("perks", styleType, self.styleNames[style], \
                                    "/perk" + str(perk) + "_" + self.lossFunction)
   
    def _getPerkStyleModelName(self, modelType)-> str:
        return "perkstyle/" + modelType + "_perkstyle_" + self.lossFunction

    def _getStyleModel(self, modelType: str)-> Model:
        if modelType not in self.styleModels:
            self.styleModels[modelType] = Model(self.netConfigDir, self.modelDir, \
                           self._getPerkStyleModelName(modelType))
        return self.styleModels[modelType]


