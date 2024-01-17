import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

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

# URL of the page you want to scrape
url = "https://psut.edu.jo/en/student-life-clubs"

# Call the function with the URL
result_club_data = scrape_club_information(url)

# Check if the result_club_data is not None before saving to a JSON file
if result_club_data is not None:
    output_directory = '/tmp/output'

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Save the extracted data to a JSON file in the specified directory
    json_file_path_club = os.path.join(output_directory, 'club_information.json')
    with open(json_file_path_club, 'w', encoding='utf-8') as json_file_club:
        json.dump(result_club_data, json_file_club, ensure_ascii=False, indent=2)

    # Print the path to the saved JSON file
    print(f'Data saved to: {json_file_path_club}')
else:
    print("No data to save.")
result_club_data = scrape_club_information(url)

# Check if the result_club_data is not None
if result_club_data is not None:
    # Print the data
    print(result_club_data)
else:
    print("No data to save.")


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
