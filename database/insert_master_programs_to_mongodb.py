import requests
from bs4 import BeautifulSoup
import json
import os
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']
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
                " master_Program_Name": program_name,
                "master_Program_Description": program_description,
        
            })

    return program_data

# Example URL
url_master_programs = "https://psut.edu.jo/en/school/School_of_Graduate_Studies_Scientific_Research"

# Call the function to scrape master's programs information
master_programs_data = scrape_master_programs_info(url_master_programs)

# Specify the directory where you have write permissions
output_directory = '/tmp/output_school'

# Ensure the directory exists
os.makedirs(output_directory, exist_ok=True)

# Specify the output JSON file path
output_json_file = os.path.join(output_directory, 'master_programs_data.json')

# Save the extracted data to a JSON file
with open(output_json_file, 'w', encoding='utf-8') as json_file:
    json.dump(master_programs_data, json_file, ensure_ascii=False, indent=2)

print(f'Data saved to: {output_json_file}')


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
