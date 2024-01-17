from pymongo import MongoClient, UpdateOne

# Initialize MongoDB client
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient, UpdateOne

def scrape_departments(department_container):
    departments = department_container.find_all("a", href=True)

    department_data = []
    for department in departments:
        department_name = department.find("h4").text.strip()
        department_data.append({
            "Department Name": department_name
        })

    return department_data

def scrape_bachelors_programs(program_container):
    programs = program_container.find_all("a", href=True)

    program_data = []
    for program in programs:
        program_name = program.find("h4").text.strip()
        program_description = program.find("p").text.strip()
        program_data.append({
            "Bachelors Program Name": program_name,
            "Bachelors Program Description": program_description,
        })

    return program_data

def scrape_school_info(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        department_container = soup.find("div", class_="tab-pane fade show active")
        program_container = soup.find("div", class_="tab-pane fade show active")

        department_data = scrape_departments(department_container)
        program_data = scrape_bachelors_programs(program_container)

        return department_data, program_data

    else:
        print(f"Failed to retrieve the page for URL: {url}")
        return None, None

departments_collection = db['Departments']
bachelors_programs_collection = db['Bachelors Programs']  # Updated collection name

# Example URLs
urls_list = [
    "https://psut.edu.jo/en/school/School_of_Engineering",
    "https://psut.edu.jo/en/school/King_business_technology",
    "https://psut.edu.jo/en/school/school_of_computing_sciences#nav-home"
]

# Separate data for all URLs
all_department_data = []
all_bachelors_program_data = []

for url in urls_list:
    department_data, bachelors_program_data = scrape_school_info(url)
    
    if department_data:
        all_department_data.extend(department_data)
        
        # Update or insert data into MongoDB using UpdateOne with upsert
        for data in department_data:
            filter_condition = {"Department Name": data["Department Name"]}
            update_operation = UpdateOne(
                filter_condition,
                {"$set": data},
                upsert=True
            )
            departments_collection.bulk_write([update_operation])
    
    if bachelors_program_data:
        all_bachelors_program_data.extend(bachelors_program_data)
        
        # Update or insert data into MongoDB using UpdateOne with upsert
        for data in bachelors_program_data:
            filter_condition = {"Bachelors Program Name": data["Bachelors Program Name"]}
            update_operation = UpdateOne(
                filter_condition,
                {"$set": data},
                upsert=True
            )
            bachelors_programs_collection.bulk_write([update_operation])

print("Data saved to MongoDB.")
