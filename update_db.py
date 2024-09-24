import sys
from pymongo import MongoClient
from bson.objectid import ObjectId

mongo_id_strs = sys.argv[1:]
mongo_ids = [ObjectId(mongo_id_str) for mongo_id_str in mongo_id_strs]
client = MongoClient('mongodb://localhost:27017/')
db = client['stockalerts']
collection = db['stocks']

for mongo_id in mongo_ids:
    result = collection.update_one(
        {"_id": mongo_id},
        {"$set": {"status": "Triggered"}}
    )

client.close()