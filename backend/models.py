from keras.models import load_model, model_from_json
import json
import os.path as path
from typing import List, Mapping
import keras.backend as K
import keras.metrics as metrics
import pickle
import perks.get_smarties as get_smarties
import sys
# THIS IS AN EVIL HACK TO MAKE PICKLE LIKE US
# TL;DR: pickle requires the class to stay in the same package at the samle location
# we can't do this. therefore we set the old smarties package (perks.get_smarties, see ml/)
# to the new get_smarties
sys.modules["perks.get_smarties"] = get_smarties
sys.modules["get_smarties"] = get_smarties

# TODO: no lazy loading, instead load at application start time

def makeTopKAccuracy(k):
    def topKAccuracy(y_true, y_pred): 
        return metrics.top_k_categorical_accuracy(y_true, y_pred, k)
    return topKAccuracy

def maskedErrorFunc(y_true, y_pred):
    mask = K.cast(K.not_equal(y_true, -1), K.floatx())
    maskedError = (y_true - y_pred) * mask
    correct = K.mean(K.square(maskedError))
    return correct

import tensorflow as tf
#global graph
#graph = tf.get_default_graph();

# netConfigName is path from netConfig dir (RELATIVE to netConfig Dir) to the json file
class Model:
    def __init__(self, netConfigsDir, modelDir, netConfigName):
        self.netConfig = self._loadNetConfig(netConfigsDir, netConfigName)
        self.topKAccuracy = makeTopKAccuracy(self.netConfig["top_k_parameter"])
        self.smarties = self._loadSmarties(modelDir, self._getModelName())
        print("Loading model")
        self.model = self.loadModel(modelDir, self._getModelName())
        self.graph = tf.get_default_graph()

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
        print("Reading architecture")
        architecture = path.join(modelDir, modelFile, "architecture");
        with open(architecture, 'r') as architectureFile:
            architecture = json.load(architectureFile)
        print("Loading architecture")
        model = model_from_json(architecture)
        print("Loaded model")
        weights = path.join(modelDir, modelFile, "weights");
        print("got weights")
        model.load_weights(weights)
        print("loading weights")
        return model

    def getColumns(self, data, columns):
        dfCols = data.columns
        cols = []
        for dfCol in dfCols.values:
            for column in columns:
                # either same OR we found the start of a nominal value
                if dfCol == column or dfCol.startswith(column + "_"): 
                    cols.append(dfCol)
        return cols

    def predict(self, fullData):
        print(fullData.columns)
        transformed = self.smarties.transform(fullData)
        transformed.reindex_axis(sorted(transformed.columns), axis=1)
        inputCols = self.getColumns(transformed, self.netConfig["columns"])
        inputCols = sorted(inputCols)
        input = transformed[inputCols]
        with self.graph.as_default():
            output =  self.model.predict(input.values)[0].tolist()
        print("Predict column:" + self.netConfig["predictColumn"])
        outputCols = self.getColumns(transformed, [self.netConfig["predictColumn"]])
        print(outputCols)
        outputCols = sorted(outputCols)
        result = list(zip(outputCols, output))
        return result

    def _selectSubsetData(self, fullData):
        pass

import tensorflow as tf
class Models:
    
    def __init__(self, netConfigDir, modelDir, lossFunction, styleNames: Mapping[int, str] ):
        self.netConfigDir = netConfigDir
        self.modelDir = modelDir
        self.lossFunction = lossFunction
        self.styleModels = {}
        self.perkModels = {}
        self.styleNames = styleNames
        self._initAllModels()


    def _initAllModels(self):
        self.getPrimaryStyleModel()
        self.getSubStyleModel()
        for style in [8000, 8100, 8200, 8300, 8400]:
            for perk in [0,1,2,3]:
                self.getPrimaryStyleRunesModel(style, perk)
        for subStyle in [8000, 8100, 8200, 8300, 8400]:
            for perk in [4,5]:
                self.getSubStyleRunesModel(subStyle, perk)
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
            self.perkModels[str(style)][str(perk)] = Model(self.netConfigDir, self.modelDir, modelName)
        return self.perkModels[str(style)][str(perk)]

    def _getPerkModelName(self, styleType: str, style: int, perk: int)-> str:
        print("Input: " + styleType + ", " + str(style) + ", " + str(perk))
        model =  path.join("perks", styleType, self.styleNames[style], "perk" + str(perk) + "_" + self.lossFunction + ".json")
        print("Loading model from " + model)
        return model
   
    def _getPerkStyleModelName(self, modelType)-> str:
        model =  "perkstyle/" + modelType + "_perkstyle_" + self.lossFunction
        print("Loading model from " + model)
        return model

    def _getStyleModel(self, modelType: str)-> Model:
        if modelType not in self.styleModels:
            self.styleModels[modelType] = Model(self.netConfigDir, self.modelDir, \
                           self._getPerkStyleModelName(modelType) + ".json")
        return self.styleModels[modelType]


