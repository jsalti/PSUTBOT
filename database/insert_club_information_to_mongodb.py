# -*- coding: utf-8 -*-
"""insert_club_information_to_mongodb.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N7g_JSpmYC00i-daaXMGfhLdlxQKmeiP
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install pymongo

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
# Choose or create a database
db = client['PSUTBOT_database_1']

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
    documents = [{"Club Name": name, "Description": description} for name, description in zip(data["Club Name"], data["Description"])]

    # Insert JSON data into MongoDB
    collection.insert_many(documents)

    print("Data inserted successfully!")

# Example usage
url = "https://psut.edu.jo/en/student-life-clubs"
result_club_data = scrape_club_information(url)

# Check if the result_club_data is not None
if result_club_data is not None:
    collection_name_club = 'Club information'  # Update with your actual collection name
    insert_club_information_to_mongodb(result_club_data, db, collection_name_club)
else:
    print("No data to insert.")