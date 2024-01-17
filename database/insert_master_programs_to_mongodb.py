import requests
from bs4 import BeautifulSoup
import json
import os
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']
def insert_master_programs_to_mongodb(data, db, collection_name):
    """
    Inserts master's programs information into MongoDB.

    Parameters:
        data (list): List of dictionaries containing master's programs information.
        db: MongoDB database object.
        collection_name (str): Name of the collection to insert data into.
    """
    # Create a collection
    collection_master_programs=db['Masters_programs']
    # Insert JSON data into MongoDB
    collection_master_programs.insert_many(data)

    print("Data inserted successfully!")

# Example usage
collection_name_master_programs = 'Masters Programs'  # Update with your actual collection name

# Load the JSON data from the file
with open(output_json_file, 'r', encoding='utf-8') as file:
    master_programs_data = json.load(file)

# Call the function to insert data into MongoDB
insert_master_programs_to_mongodb(master_programs_data, db, collection_name_master_programs)

print("Master's programs data inserted successfully into MongoDB!")
