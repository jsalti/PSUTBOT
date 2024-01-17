from pymongo import MongoClient, UpdateOne
from scripts.scrape_master_programs_info import scrape_master_programs_info

# Initialize MongoDB client
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']

import requests
from bs4 import BeautifulSoup
import json
import os


def scrape_master_programs_info(url):
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup_master_programs = BeautifulSoup(html_content, "html.parser")

    # Find the container for the program information
    program_container = soup_master_programs.find("div", class_="tab-pane fade show active")

    # Extract information about programs
    programs = program_container.find_all("a", href=True)

    program_data = []
    for program in programs:
        program_name_tag = program.find("h4")
        program_description_tag = program.find("p")

        if program_name_tag and program_description_tag:
            program_name = program_name_tag.text.strip()
            program_description = program_description_tag.text.strip()
            program_data.append({
                "Master Program Name": program_name,
                "Master Program Description": program_description,
            })

    return program_data

# Example URL
url_master_programs = "https://psut.edu.jo/en/school/School_of_Graduate_Studies_Scientific_Research"

# Call the function to scrape master's programs information
master_programs_data = scrape_master_programs_info(url_master_programs)

# Specify the MongoDB connection details
client = MongoClient('mongodb://localhost:27017/')
db = client['PSUTBOT']

def insert_master_programs_to_mongodb(data, db, collection_name):
    """
    Inserts or updates master's programs information into MongoDB.

    Parameters:
        data (list): List of dictionaries containing master's programs information.
        db: MongoDB database object.
        collection_name (str): Name of the collection to insert data into.
    """
    # Create a collection
    collection = db[collection_name]

    # Update or insert data into MongoDB using UpdateOne with upsert
    operations = [UpdateOne(
        {"Master Program Name": item["Master Program Name"]},
        {"$set": item},
        upsert=True
    ) for item in data]

    collection.bulk_write(operations)
    print("Master's programs data inserted or updated successfully into MongoDB!")

# Example usage
collection_name_master_programs = 'Masters Programs'  # Update with your actual collection name

# Call the function to insert or update data into MongoDB
insert_master_programs_to_mongodb(master_programs_data, db, collection_name_master_programs)

