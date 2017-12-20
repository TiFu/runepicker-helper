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

from preprocessing import fetchData, preprocessDataForRandomForest

rows = fetchData(connection, netConfig["columns"], netConfig["predictColumn"], netConfig["perkstyle_attribute"], netConfig["perkstyle"])
processedData = preprocessDataForRandomForest(rows, netConfig["columns"], netConfig["predictColumn"], netConfig["nominalColumns"])

from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier

y = processedData.transformed_rows[netConfig["predictColumn"]]
x = processedData.transformed_rows[processedData.getColumns(netConfig["columns"])]

clf = RandomForestClassifier()
clf.fit(x, y)

predictY = clf.predict(x)

print( accuracy_score(y, predictY) )
testReport = classification_report(y, predictY)
print(testReport)
