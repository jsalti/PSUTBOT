from pymongo import MongoClient, UpdateOne

# Initialize MongoDB client
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']

import pandas as pd
from pymongo import MongoClient
import json

def insert_BusSchedule_to_mongodb(json_file_path, db, collection_name):
    """
    Insert JSON data into MongoDB.

    Parameters:
        json_file_path (str): Path to the JSON file.
        db: MongoDB database object.
        collection_name (str): Name of the collection to insert data into.
    """
    # Create a collection
    collection_bus_Schedule= db['bus_Schedul']

    # Load the entire JSON data from the file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_data_list = [json.loads(line) for line in file]

    # Insert JSON data into MongoDB using insert_many
    collection.insert_many(json_data_list)

    print("Data inserted successfully into MongoDB!")

# Example usage
csv_file_path = r"C:\Users\BASIL\Desktop\BusSchedule.csv"
json_file_path = r'C:\Users\BASIL\Desktop\BusSchedule.json'
collection_name_bus_schedule = 'bus_Schedule'  # Update with your actual collection name

# Convert CSV to JSON
convert_csv_to_json(csv_file_path, json_file_path)

# Insert JSON data into MongoDB
insert_BusSchedule_to_mongodb(json_file_path, db, collection_name_bus_schedule)

