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
            "club_Description": club_descriptions
        }

        return data  # Return the data dictionary

    else:
        print("Failed to retrieve the page.")
        return None

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
    documents = [{"Club_Name": name, "club_Description": description} for name, description in zip(data["Club Name"], data["club_Description"])]

    # Insert JSON data into MongoDB
    collection.insert_many(documents)

    print("Data inserted successfully!")

if __name__ == "__main__":
    action = sys.argv[1]

    if action == "--get-code-before":
        # Implement code extraction here if needed
        pass
    elif action == "--scrape-club-data":
        url = "https://psut.edu.jo/en/student-life-clubs"
        result_club_data = scrape_club_information(url)
        print(json.dumps(result_club_data))
    elif action == "--insert-into-mongodb":
        data = json.loads(os.environ['SCRAPE_RESULT'])
        db_name = os.environ['DB_NAME']
        client = MongoClient()
        db = client[db_name]
        collection_name_club = 'Club information'
        insert_club_information_to_mongodb(data, db, collection_name_club)
