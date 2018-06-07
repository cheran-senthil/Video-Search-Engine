import glob
import json
import os

import pymongo

import common

# Creates a new database
collection = common.getCollection('localhost', "videodb", "videos")
collection.drop()

# Gets all json files in test
os.chdir("./test")
json_file_names = glob.glob("*.json")

# Uplods all data to mongodb
for json_file_name in json_file_names:
    # Loads the json file
    json_file = open(json_file_name)
    data = json.load(json_file)

    # Uplods data to mongodb
    collection.insert_one(data)

print collection.count(), "file inserted to mongodb"
