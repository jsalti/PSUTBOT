from pymongo import MongoClient, UpdateOne

# Initialize MongoDB client
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']

import json
from pymongo import MongoClient

# MongoDB Configuration
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["PSUTBOT"]
collection = db["Academic_Calendar"]

# Load the extracted text from the JSON file
json_file_path = '/tmp/output_academic_calendar/academic_calendar_text.json'
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    academic_calendar_data = json.load(json_file)

# Insert the combined data into MongoDB
document = {"academic_calendar_information": academic_calendar_data["Text"]}
collection.insert_one(document)
print('Combined table inserted into MongoDB')
