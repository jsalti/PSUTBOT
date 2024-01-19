import requests
from bs4 import BeautifulSoup
import json
import os
import sys
from pymongo import MongoClient

def scrape_departments(department_container):
    departments = department_container.find_all("a", href=True)

    department_data = []
    for department in departments:
        department_name = department.find("h4").text.strip()
        department_data.append({
            "Department Name": department_name
        })

    return department_data

def scrape_programs(program_container):
    programs = program_container.find_all("a", href=True)

    program_data = []
    for program in programs:
        program_name = program.find("h4").text.strip()
        program_description = program.find("p").text.strip()
        program_data.append({
            "Program_Name": program_name,
            "program_Description": program_description,
        })

    return program_data

def scrape_school_info(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the container for the department information
        department_container = soup.find("div", class_="tab-pane fade show active")

        # Extract information about departments
        department_data = scrape_departments(department_container)

        # Find the container for the program information
        program_container = soup.find("div", class_="tab-pane fade show active")

        # Extract information about programs
        program_data = scrape_programs(program_container)

        return department_data, program_data

    else:
        print(f"Failed to retrieve the page for URL: {url}")
        return None, None

def save_to_mongodb(data, collection, db):
    # Insert data into MongoDB
    collection.insert_many(data)
    print(f"Data inserted successfully into {collection.name} collection.")

if __name__ == "__main__":
    action = sys.argv[1]

    # Connect to MongoDB
    client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
    db = client['PSUTBOT']  # Replace 'your_database_name' with your actual database name

    # Create collections
    departments_collection = db['Departments']
    programs_collection = db['Programs']

    # Example URLs
    urls_list = [
        "https://psut.edu.jo/en/school/School_of_Engineering",
        "https://psut.edu.jo/en/school/King_business_technology",
        "https://psut.edu.jo/en/school/school_of_computing_sciences#nav-home"
    ]

    # Separate data for all URLs
    all_department_data = []
    all_program_data = []

    if action == "--scrape-and-insert":
        for url in urls_list:
            department_data, program_data = scrape_school_info(url)

            if department_data:
                all_department_data.extend(department_data)
                save_to_mongodb(department_data, departments_collection, db)

            if program_data:
                all_program_data.extend(program_data)
                save_to_mongodb(program_data, programs_collection, db)

        print("Data saved to MongoDB.")

    elif action == "--get-code-before":
        # Implement code extraction here if needed
        pass

    else:
        print("Invalid action. Use --scrape-and-insert or --get-code-before.")
