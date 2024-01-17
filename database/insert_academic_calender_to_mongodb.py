from pymongo import MongoClient, UpdateOne
import json

def insert_then_update_academic_calendar_data(json_file_path, collection_name):
    # Initialize MongoDB client for Atlas cluster
    atlas_client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
    atlas_db = atlas_client['PSUTBOT']
    atlas_collection = atlas_db[collection_name]

    # Load the extracted text from the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        academic_calendar_data = json.load(json_file)

    # Specify the filter based on the content of the loaded JSON file
    filter_query = {"academic_calendar_information": academic_calendar_data["Text"]}

    # Specify the update content
    update_content = {"$set": {"academic_calendar_information": academic_calendar_data["Text"]}}

    # Attempt insert
    atlas_collection.insert_one(filter_query)

    # Create an UpdateOne operation to handle the case where the document already exists
    update_operation = UpdateOne(filter_query, update_content)

    # Execute the update operation
    result = atlas_collection.bulk_write([update_operation])

    print(f'Matched Count: {result.matched_count}')
    print(f'Modified Count: {result.modified_count}')
    print('Combined table inserted or updated in MongoDB')
json_file_path = '/tmp/output_academic_calendar/academic_calendar_text.json'
collection_name = 'Academic Calendar'
insert_then_update_academic_calendar_data(json_file_path, collection_name)
)
