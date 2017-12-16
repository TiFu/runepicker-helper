import database
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

class Data:
    
    def __init__(self, originalDataFrame, transformedDataFrame, totalColumns):
        self.original_rows = originalDataFrame
        self.transformed_rows = transformedDataFrame
        self.totalColumns = totalColumns

    def transform(self, rows):
        df1 = pd.get_dummies(self.makeDataFrame(rows))
        df1.reindex(columns = self.transformed_rows.columns, fill_value=0)
        return df1

    # maybe more efficient implementation.. not an important isuse though
    def getColumnCount(self, columns, startAt = 0):
        dfCols = self.transformed_rows.columns
        i = startAt
        colCount = 0
        for dfCol in dfCols.values:
            for column in columns:
                # either same OR we found the start of a nominal value
                if dfCol == column or dfCol.startswith(column + "_"): 
                    colCount += 1
        print("-----------------")
        return colCount

    def makeDataFrame(self, rows):
        df = pd.DataFrame(rows, columns=self.totalColumns)
        return df

def fetchData(connection, columns, predictColumn):
    cursor = connection.cursor()
    cursor.execute("SELECT " + ", ".join(map(lambda x: "\"" + x + "\"", columns)) + ", \"" + predictColumn + """\" FROM style_prediction_data""");
    rows = cursor.fetchall()
    cursor.close()
    return rows

def preprocessData(rows, columns, predictColumn, nominalColumns):
    totalColumns = []
    totalColumns.extend(columns)
    totalColumns.append(predictColumn)
    dataFrame = pd.DataFrame(rows, columns=totalColumns)
    dummies = pd.get_dummies(data=dataFrame, columns=nominalColumns)
    return Data(dataFrame, dummies, totalColumns)
