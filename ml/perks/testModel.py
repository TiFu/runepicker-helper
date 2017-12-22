# first arg: netconfig
import psycopg2
import json
import sys
from neuralnet import load
from preprocessing import fetchData, fetchDataFiltered, preprocessData
import database
from config import config
import numpy as np

# Database
dbConfig = config["database"]
url = dbConfig["url"]
user = dbConfig["username"]
password = dbConfig["password"]
db = dbConfig["database"]
connection = database.connect(url, user, password,db)

# Net config
from .netconfig import loadNetconfig
netConfig = loadNetConfig(sys.argv[1])

# Model
model = load(netConfig)

# Original Data
rows = fetchData(connection, netConfig["columns"], netConfig["predictColumn"])
trainData = preprocessData(rows, netConfig["columns"], netConfig["predictColumn"], netConfig["nominalColumns"])

# Data
rows = fetchDataFiltered(connection, netConfig["columns"], netConfig["predictColumn"], [("champion_id", 81)])
data = trainData.transform(rows)
print(data.columns)
inCols = trainData.getColumns(netConfig["columns"]);
outCols = trainData.getColumns([netConfig["predictColumn"]])
dataX = data[inCols]
print(str(len(inCols)) + ": " + str(dataX.columns))
dataY = data[outCols];
print(str(len(outCols)) + ": " + str(dataY.columns))

# Predict and Report
predictY = model.predict_classes(dataX.values)
from sklearn.metrics import classification_report
report = classification_report(np.argmax(dataY.values, axis=1), predictY)

print(report)