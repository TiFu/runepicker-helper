from keras.models import load_model
import json
import os.path as path
from typing import List, Map
class Models:
    
    def __init__(self, netConfigDir, modelDir, lossFunction, styleNames: Map[int, str] ):
        self.netConfigDir = netConfigDir
        self.modelDir = modelDir
        self.lossFunction = lossFunction
        self.styleModels = {}
        self.perkModels = {}
        self.styleNames = styleNames

    def getPrimaryStyleModel(self): -> Model
        return self._getStyleModel("primary");

    def getSubStyleModel(self): -> Model
        return self._getStyleModel("sub");

    def getPrimaryStyleRunesModel(self, primaryStyle: int, perk: int): -> Model
        return self._getPerkModel("primary", primaryStyle, perk);

    def getSubStyleRunesModel(self, subStyle: int, perk: int): -> Model
        return self._getPerkModel("secondary", subStyle, perk);

    def _getPerkModel(self, styleType: str, style: int, perk: int): -> Model
        if styleType not in self.perkModels:
            self.perkModels[styleType] = {}
        if str(style) not in self.perkModels:
            self.perkModels[str(style)] = {}
        if str(perk) not in self.perkModels[str(style)]:
            modelName = self._getPerkModelName(styleType, style, perk)
            self.perkModels = Model(self.netConfigDir, self.modelDir, modelName)
        return self.perkModels[str(style)][str(perk)]

    def _getPerkModelName(self, styleType: str, style: int, perk: int): -> str
        return path.join("perks", styleType, self.styleNames[style], \
                                    "/perk" + str(perk) + "_" + self.lossFunction)
   
    def _getPerkStyleModelName(self, modelType): -> str
        return "perkstyle/" + modelType + "_perkstyle_" + self.lossFunction

    def _getStyleModel(self, modelType: str): -> Model
        if modelType not in self.styleModels:
            self.styleModels[modelType] = Model(self.netConfigDir, self.modelDir, \
                           self._getPerkStyleModelName(modelType))
        return self.styleModels[modelType]


class Model:
    
    def __init__(self, netConfigsDir, modelDir, netConfigName):
        self.netConfig = self._loadNetConfig(netConfigsDir, netConfigName)
        self.model = self.loadModel(modelDir, self._getModelDir())

    def _getModelDir(self):
        return self.netConfig["directory"]
    
    def _loadNetConfig(self, netConfigsDir, netConfigName):
        netConfig = json.load(open(path.join(netConfigsDir, netConfigName)))
        netConfig["directory"] = netConfigName.replace(".json", "")
        return netConfig

    def loadModel(self, modelDir, modelFile):
        modelFile = path.join(modelDir, modelFile, "model");
        return load_model(modelFile)

    # TODO: decide on data structure
    def predict(self, fullData):
        # TODO: select columns, predict and return with column names or so
        # needs copy of neural net code
        pass

    def _selectSubsetData(self, fullData):
        pass