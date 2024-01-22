import os
import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient
import sys

def scrape_club_information(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the relevant HTML elements containing the club information
        club_elements = soup.find_all("div", class_="col-md-6 col-lg-3")

        # Create lists to store club information
        club_names = []
        club_descriptions = []

        # Extract information and populate lists
        for club in club_elements:
            club_name = club.find("h5").find("a").text.strip()
            club_description = club.find("p").text.strip()

            club_names.append(club_name)
            club_descriptions.append(club_description)

        # Create a dictionary from the lists
        data = {
            "Club Name": club_names,
            "Club Description": club_descriptions
        }

        return data  # Return the data dictionary

    else:
        print("Failed to retrieve the page.")
        return None

def insert_club_information_to_mongodb(data, db, collection_name):

    # Create a collection
    collection = db[collection_name]

    # Convert the dictionary to a list of documents
    documents = [{"_id": name, "Club Name": name, "Club Description": description} for name, description in zip(data["Club Name"], data["Club Description"])]

    # Update existing documents or insert new ones based on '_id' field
    for document in documents:
        filter_criteria = {"_id": document["_id"]}
        update_data = {"$set": document}
        collection.update_many(filter_criteria, update_data, upsert=True)

    print("Data inserted or updated successfully!")

def extract_code_before_club():
    # Add your code extraction logic here for club information
    print("Code extraction logic for club information goes here.")

if __name__ == "__main__":
    action = sys.argv[1]

    url = "https://psut.edu.jo/en/student-life-clubs"

    # MongoDB Configuration
    mongo_client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
    db = mongo_client['PSUTBOT']
    collection_name_club = 'Club Information'

    if action == "--scrape-club-data":
        result_club_data = scrape_club_information(url)
        print(json.dumps(result_club_data))

    elif action == "--insert-into-mongodb":
        data = json.loads(os.environ['SCRAPE_RESULT'])
        insert_club_information_to_mongodb(data, db, collection_name_club)

    elif action == "--get-code-before":
        # Implement code extraction logic for club information if needed
        extract_code_before_club()

    else:
        print("Invalid action. Use --scrape-club-data, --insert-into-mongodb, or --get-code-before.")
