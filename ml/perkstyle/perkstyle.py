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
netConfig = json.load(open("./perkstyle/netconfig/" + sys.argv[1]))

from preprocessing import fetchData, preprocessData

rows = fetchData(connection, netConfig["columns"], netConfig["predictColumn"])
processedData = preprocessData(rows, netConfig["columns"], netConfig["predictColumn"], netConfig["nominalColumns"])
data = processedData.transformed_rows
print(data.columns)

# TODO: integrate netConfig and this code into preprocessing.Data
# train data length & col counts
trainValidData = int(netConfig["trainDataPercentage"] * len(rows))
inCols = processedData.getColumns(netConfig["columns"]);
outCols = processedData.getColumns([netConfig["predictColumn"]])
netConfig["layers"][0]["inputDim"] = len(inCols)

# train/val & test data
trainX = data.iloc[0:trainValidData,:][inCols]
trainY = data.iloc[0:trainValidData,:][outCols];
testX = data.iloc[trainValidData:len(rows),:][inCols]
testY = data.iloc[trainValidData:len(rows),:][outCols];

print("Input columns (" + str(len(inCols)) + "): " + str(trainX.columns))
print("Target columns ( " + str(len(outCols)) + "): " + str(trainY.columns))


from neuralnet import build, train, save
model = build(netConfig)
history = train(model, trainX, trainY, netConfig)

from sklearn.metrics import classification_report
predictY = model.predict_classes(testX.values)
predictTrainY = model.predict_classes(trainX.values)
print("")
print("Training Data: ")
trainReport = classification_report(np.argmax(trainY.values, axis=1), predictTrainY)
print(trainReport)
print("Test data:")
testReport = classification_report(np.argmax(testY.values, axis=1), predictY)
print(testReport)
# TODO: save classification report and graph for train & validation loss
save(model, history, netConfig, trainReport, testReport)