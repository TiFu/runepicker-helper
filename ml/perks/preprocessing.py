import database
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from get_smarties import Smarties
class Data:
    
    def __init__(self, smarties, originalDataFrame, transformedDataFrame, totalColumns):
        self.original_rows = originalDataFrame
        self.transformed_rows = transformedDataFrame
        self.totalColumns = totalColumns
        self.smarties = smarties

    def transform(self, rows):
        df1 = self.smarties.transform(self.makeDataFrame(rows))
        return df1

    def getColumns(self, columns):
        dfCols = self.transformed_rows.columns
        cols = []
        for dfCol in dfCols.values:
            for column in columns:
                # either same OR we found the start of a nominal value
                if dfCol == column or dfCol.startswith(column + "_"): 
                    cols.append(dfCol)
        return cols

    def makeDataFrame(self, rows):
        df = pd.DataFrame(rows, columns=self.totalColumns)
        return df
        
# integraet into fetchData?
#def fetchDataFiltered(connection, columns, predictColumn, conditions):
#    cursor = connection.cursor()
#    conditions = map(lambda x: x[0] + " = " + "'" +  str(x[1]) + "'", conditions)
#    cursor.execute("SELECT " + ", ".join(map(lambda x: "\"" + x + "\"", columns))\
#                    + ", \"" + predictColumn + "\", \"win\" FROM style_prediction_data WHERE " \
#                    + " and ".join(conditions));
#    rows = cursor.fetchall()
#    cursor.close()
#    return rows

def fetchData(connection, columns, predictColumn, perkstyle_attribute, perkstyle):
    cursor = connection.cursor()
    cursor.execute("SELECT " + ", ".join(map(lambda x: "\"" + x + "\"", columns)) + ", \"" + predictColumn + "\", \"win\" FROM style_prediction_data WHERE " + perkstyle_attribute + " = " + str(perkstyle));
    rows = cursor.fetchall()
    cursor.close()
    return rows

# TODO: use https://github.com/pandas-dev/pandas/issues/8918
#       see comment of jreback on Oct 5, 2015 (and determine automatically)
def preprocessData(rows, columns, predictColumn, nominalColumns, netConfig):
    totalColumns = []
    totalColumns.extend(columns)
    totalColumns.append(predictColumn)
    totalColumns.append("win")
    dataFrame = pd.DataFrame(rows, columns=totalColumns)
    dataFrame["win"] = pd.to_numeric(dataFrame["win"])
    smarties = Smarties()
    dummies = smarties.fit_transform(data=dataFrame, columns=nominalColumns)
    # TODO: set 1 or -1 depending on win 
    data = Data(smarties, dataFrame, dummies, totalColumns)
    cols = data.getColumns([predictColumn])
    if netConfig["loss"] == "win_loss":
        for col in cols:
            # set 'not picked' perks to -1
            data.transformed_rows[col] = np.where(data.transformed_rows[col] == 0, -1, data.transformed_rows[col])
            # set to 1 if won and picked
            # TODO: exclude -1 from this setting 
            data.transformed_rows[col] = np.where(data.transformed_rows[col] > -1, data.transformed_rows["win"], -1)
    return data

from sklearn import preprocessing
def preprocessDataForRandomForest(rows, columns, predictColumn, nominalColumns):
    totalColumns = []
    totalColumns.extend(columns)
    totalColumns.append(predictColumn)
    totalColumns.append("win")
    dataFrame = pd.DataFrame(rows, columns=totalColumns)
    dataFrame["win"] = pd.to_numeric(dataFrame["win"])
    for col in nominalColumns:
        le = preprocessing.LabelEncoder()
        dataFrame[col].fillna(value="null", inplace=True) 
        dataFrame[col] = le.fit_transform(dataFrame[col])
    
    data = Data(None, dataFrame, dataFrame, totalColumns)
    return data