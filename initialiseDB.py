import os

from nlpUtils import TextSimilarity
import json

import pymongo
from pymongo import MongoClient
import urllib.parse


import xlrd
 
loc = ("Dataset.xlsx")
 
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)

#text:'id', text:'quotes', text:'author', text:'source', text:'rating', text:'addedBy']
completeCells = [{"id":sheet.cell_value(i, 0), \
    "quotes": sheet.cell_value(i, 1), \
    "author": sheet.cell_value(i, 2), \
    "source": sheet.cell_value(i, 3), \
    "rating": sheet.cell_value(i, 4), \
    "addedBy": sheet.cell_value(i, 5), \
            }for i in range(sheet.nrows)]

# for i in range(sheet.nrows):
#     print(sheet.cell_value(i, 1))
print(completeCells)

username = urllib.parse.quote_plus(os.environ.get('MONGO_DB_USERNAME'))
password = urllib.parse.quote_plus(os.environ.get('MONGO_DB_PASSWORD'))

client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@cluster0.017ba.mongodb.net/quote?retryWrites=true&w=majority")
db = client.quotes
quote_collection = db.quotes
quote_collection.drop()
quote_collection.insert_many(completeCells).inserted_ids

print(quote_collection.count_documents({}))
