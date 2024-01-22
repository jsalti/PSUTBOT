import requests
from bs4 import BeautifulSoup
import json
import os
from pymongo import MongoClient
import sys

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
                "master_Program_Name": program_name,
                "master_Program_Description": program_description,
            })

    return program_data

def save_to_json(data, output_directory, filename):
    # Save the extracted data to a JSON file in the specified directory
    output_json_file = os.path.join(output_directory, filename)
    with open(output_json_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

    # Print the path to the saved JSON file
    print(f'Data saved to: {output_json_file}')

def insert_master_programs_to_mongodb(data, db, collection_name):
    # Create a collection
    collection_master_programs = db[collection_name]

    # Update existing documents or insert new ones if they don't exist
    for document in data:
        filter_query = {"master_Program_Name": document["master_Program_Name"]}  # Assuming "master_Program_Name" is unique
        update_operation = {
            "$set": document
        }

        collection_master_programs.update_many(filter_query, update_operation, upsert=True)

    print("Data inserted or updated successfully in MongoDB!")

def extract_code_before():
    # Add your code extraction logic here
    print("Code extraction logic goes here.")

if __name__ == "__main__":
    action = sys.argv[1]

    # Example URL
    url_master_programs = "https://psut.edu.jo/en/school/School_of_Graduate_Studies_Scientific_Research"

    # Specify the directory where you have write permissions
    output_directory = '/tmp/output_school'

    # Ensure the directory exists
    os.makedirs(output_directory, exist_ok=True)

    if action == "--scrape-master-programs":
        # Call the function to scrape master's programs information
        master_programs_data = scrape_master_programs_info(url_master_programs)

        # Save data to a JSON file
        save_to_json(master_programs_data, output_directory, 'master_programs_data.json')

        # MongoDB Configuration
        mongo_client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
        db = mongo_client['PSUTBOT']

        # Example usage
        collection_name_master_programs = 'Master Programs'  # Update with your actual collection name

        # Load the JSON data from the file
        with open(os.path.join(output_directory, 'master_programs_data.json'), 'r', encoding='utf-8') as file:
            master_programs_data = json.load(file)

        # Call the function to insert data into MongoDB
        insert_master_programs_to_mongodb(master_programs_data, db, collection_name_master_programs)

        print("Master's programs data inserted successfully into MongoDB!")

    elif action == "--get-code-before":
        # Implement code extraction here if needed
        extract_code_before()

    else:
        print("Invalid action. Use --scrape-master-programs or --get-code-before.")
