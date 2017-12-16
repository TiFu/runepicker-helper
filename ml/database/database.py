import psycopg2
from collections import namedtuple

def connect(url, user, password,database):
    dataSrc = psycopg2.connect("dbname='" + database +  "' user='" + user + "' host='" + url + "' password='" + password + "'")
    return dataSrc;

def createRecord(cursor, rows):
    ''' given obj from db returns namedtuple with fields mapped to values '''
    fields = [desc[0] for desc in cursor.description]
    Record = namedtuple("Record", fields)
    result = []
    for row in rows:
        mappings = dict(zip(fields, row))
        result.append(Record(**mappings))
    return result