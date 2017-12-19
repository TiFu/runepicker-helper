#
#   Input arg 1: net config file
#
#
#
#
#
import sys
import json
import numpy as np
if len(sys.argv) < 2:
    print("First argument: net config file is required")

import database
from config import config

dbConfig = config["database"]
url = dbConfig["url"]
user = dbConfig["username"]
password = dbConfig["password"]
db = dbConfig["database"]

connection = database.connect(url, user, password,db)
netConfig = json.load(open("./perks/netconfig/" + sys.argv[1]))
# TODO: set custom error func here

from preprocessing import fetchData, preprocessData

rows = fetchData(connection, netConfig["columns"], netConfig["predictColumns"], netConfig["perkstyle_attribute"], netConfig["perkstyle"])
processedData = preprocessData(rows, netConfig["columns"], netConfig["predictColumns"], netConfig["nominalColumns"])
data = processedData.transformed_rows
print(data.columns)

# TODO: integrate netConfig and this code into preprocessing.Data
# train data length & col counts
trainValidData = int(netConfig["trainDataPercentage"] * len(rows))
inCols = processedData.getColumns(netConfig["columns"]);
# train/val & test data
trainX = data.iloc[0:trainValidData,:][inCols]
testX = data.iloc[trainValidData:len(rows),:][inCols]

trainY = []
testY = []
for col in netConfig["predictColumns"]:
    outCols = processedData.getColumns([col])
    trainY.append(data.iloc[0:trainValidData,:][outCols])
    testY.append(data.iloc[trainValidData:len(rows),:][outCols])
print(netConfig)
netConfig["sharedLayers"][0]["inputDim"] = len(inCols)

print("Input columns (" + str(len(inCols)) + "): " + str(trainX.columns))
for out in trainY:
    print("Target columns ( " + str(len(outCols)) + "): " + str(out.columns))


from neuralnet import build, train, save
model = build(netConfig)
history = train(model, trainX, trainY, netConfig)

from sklearn.metrics import classification_report

print("")
predictTrainY = model.predict(trainX.values)
predictY = model.predict(testX.values)
trainReports = []
testReports = []
for i in range(len(predictTrainY)):
    print("Training Data: ")
    cols = trainY[i].columns
    predictTrainY[i] = predictTrainY[i].argmax(axis=-1)
    trainReport = classification_report(np.argmax(trainY[i].values, axis=1), predictTrainY[i])
    trainReports.append((cols, trainReport))
    print(trainReport)
    print("Test data:")
    cols = testY[i].columns
    predictY[i] = predictY[i].argmax(axis=-1)
    testReport = classification_report(np.argmax(testY[i].values, axis=1), predictY[i])
    testReports.append((cols, testReport))
    print(testY[i].columns)
    print(testReport)
    print("------------")
# TODO: save classification report and graph for train & validation loss
save(model, history, netConfig, trainReports, testReports)