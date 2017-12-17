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
def fetchDataFiltered(connection, columns, predictColumn, conditions):
    cursor = connection.cursor()
    conditions = map(lambda x: x[0] + " = " + "'" +  str(x[1]) + "'", conditions)
    cursor.execute("SELECT " + ", ".join(map(lambda x: "\"" + x + "\"", columns))\
                    + ", \"" + predictColumn + "\" FROM style_prediction_data WHERE " \
                    + " and ".join(conditions));
    rows = cursor.fetchall()
    cursor.close()
    return rows

def fetchData(connection, columns, predictColumn):
    cursor = connection.cursor()
    cursor.execute("SELECT " + ", ".join(map(lambda x: "\"" + x + "\"", columns)) + ", \"" + predictColumn + """\" FROM style_prediction_data""");
    rows = cursor.fetchall()
    cursor.close()
    return rows

# TODO: use https://github.com/pandas-dev/pandas/issues/8918
#       see comment of jreback on Oct 5, 2015 (and determine automatically)
def preprocessData(rows, columns, predictColumn, nominalColumns):
    totalColumns = []
    totalColumns.extend(columns)
    totalColumns.append(predictColumn)
    dataFrame = pd.DataFrame(rows, columns=totalColumns)
    smarties = Smarties()
    dummies = smarties.fit_transform(data=dataFrame, columns=nominalColumns)
    return Data(smarties, dataFrame, dummies, totalColumns)
