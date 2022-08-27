from unicodedata import category
from pymongo import MongoClient

import credentials
import certifi

connect  = "mongodb+srv://" + credentials.MongoDB["username"] + ":" + credentials.MongoDB["password"] + "@vacadb.dfmrc.mongodb.net/?retryWrites=true&w=majority"

client   = MongoClient(connect, tlsCAFile=certifi.where())

Vacayzen = client["Vacayzen"]


for policy in list(Vacayzen.Policies.find({'category': 'FAQ'})):
    print(policy['title'] + '\n' + '\n' + policy['text'] + '\n' + '\n' +'\n')


# Vacayzen.Assets.insert_one({'title': '20-inch Bike Rental', 'description': 'DANG, DANIEL! Nice Bike!', 'price': float(10.00), 'category': 'bike'})

# for asset in list(Vacayzen.Assets.find()):
#     print(asset['title'] + ":", asset['price'])

# Vacayzen.Assets.update_many({'category': 'bike'}, { '$mul': {'price': float(1.1)}})

# for asset in list(Vacayzen.Assets.find()):
#     print(asset['title'] + ":", asset['price'])