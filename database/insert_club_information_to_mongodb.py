import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from scrape_club_information import scrape_club_information
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']
def insert_club_information_to_mongodb(data, db, collection_name):
    """
    Inserts club information into MongoDB.

    Parameters:
        data (dict): Club information data dictionary.
        db: MongoDB database object.
        collection_name (str): Name of the collection to insert data into.
    """
    # Create a collection
    collection = db[collection_name]

    # Convert the dictionary to a list of documents
    documents = [{"Club_Name": name, "Club Description": description} for name, description in zip(data["Club Name"], data["Club Description"])]

    # Insert JSON data into MongoDB
    collection.insert_many(documents)

    print("Data inserted successfully!")

url = "https://psut.edu.jo/en/student-life-clubs"
result_club_data = scrape_club_information(url)

# Check if the result_club_data is not None
if result_club_data is not None:
    collection_name_club = 'Clubs Information'  
    insert_club_information_to_mongodb(result_club_data, db, collection_name_club)
else:
    print("No data to insert.")
