from pymongo import MongoClient

# Initialize MongoDB client for Atlas cluster
atlas_client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
atlas_db = atlas_client['PSUTBOT']
atlas_collection = atlas_db['Academic Calendar']

import json

# Load the extracted text from the JSON file
json_file_path = '/tmp/output_academic_calendar/academic_calendar_text.json'
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    academic_calendar_data = json.load(json_file)

# Insert the combined data into MongoDB (using the Atlas cluster client)
document = {"academic_calendar_information": academic_calendar_data["Text"]}
atlas_collection.insert_one(document)
print('Combined table inserted into MongoDB')
