import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
import sys
from pymongo import MongoClient

def get_total_pages(base_url):
    url = base_url.format(1)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    last_page = soup.find('a', class_='page-link', string='9')

    if not last_page:
        last_page = soup.find('a', class_='page-link', string=lambda s: s and s.isdigit())

    total_pages = int(last_page['data-page']) if last_page else 1
    return total_pages

def extract_staff_info(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve content from {url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        researcher_bio_div = soup.select_one('div.researcher-bio')

        if researcher_bio_div:
            name = researcher_bio_div.select_one('h2').text.strip()
            position = researcher_bio_div.select_one('h4').text.strip()
            contact_details_div = researcher_bio_div.select_one('div.mt-3')

            telephone_element = contact_details_div.select_one('p:contains("Telephone")')
            telephone = telephone_element.text.strip().replace('Telephone:', '') if telephone_element else ''

            email_element = contact_details_div.select_one('p:contains("Email")')
            email = email_element.text.strip().replace('Email:', '') if email_element else ''

            return {
                'Name': name,
                'Position': position,
                'Telephone': telephone,
                'Email': email,
            }
        else:
            print(f"Researcher bio not found on {url}")

    except Exception as e:
        print(f"Error: {e}")
        print(f"Error occurred on {url}")

    return None

def scrape_all_staff_info(base_url):
    total_pages = get_total_pages(base_url)
    staff_info_set = set()

    for page_number in range(total_pages, 0, -1):
        url = base_url.format(page_number)
        print(f"Processing page {page_number}: {url}")

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        staff_links = soup.find_all('a', href=lambda href: href and '/en/staff/professor/' in href)

        for staff_link in staff_links:
            staff_url = f"https://www.psut.edu.jo{staff_link['href']}"
            staff_info = extract_staff_info(staff_url)

            if staff_info:
                staff_info_set.add(json.dumps(staff_info, ensure_ascii=False, indent=2))

    # Convert unique staff information back to a list
    staff_info_list = [json.loads(info) for info in staff_info_set]

    columns = ['Name', 'Position', 'Telephone', 'Email']
    df = pd.DataFrame(staff_info_list, columns=columns)

    # Specify an alternative writable directory
    output_directory_staff = '/tmp/output_staff'
    os.makedirs(output_directory_staff, exist_ok=True)

    # Save the list of staff information to a JSON file
    json_file_path = os.path.join(output_directory_staff, 'staff_info.json')
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(staff_info_list, json_file, ensure_ascii=False, indent=2)

    print(f'Data saved to: {json_file_path}')

    return df

def insert_staff_info_to_mongodb(data, db, collection_name):

    # Create a collection
    collection_staff = db[collection_name]

    # Convert DataFrame to list of dictionaries
    data_list = data.to_dict(orient='records')

    for document in data_list:
        # Use the 'Name' field as a unique identifier
        filter_query = {"Name": document["Name"]}
        update_data = {"$set": document}
        # Use 'upsert=True' to insert the document if it doesn't exist
        collection_staff.update_many(filter_query, update_data, upsert=True)

    print("Staff information inserted successfully into MongoDB!")


if __name__ == "__main__":
    action = sys.argv[1]

    # Connect to MongoDB
    client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
    db = client['PSUTBOT']  # Replace 'your_database_name' with your actual database name

    # Example URL pattern for the staff pages
    base_url = "https://www.psut.edu.jo/en/staff/professor?page={}"

    # Scrape all staff information and get DataFrame without duplicates
    result_staff_info = scrape_all_staff_info(base_url)

    if action == "--scrape-and-insert":
        # Insert data into MongoDB
        collection_name_staff = 'Staff Info'  # Update with your actual collection name
        insert_staff_info_to_mongodb(result_staff_info.to_dict(orient='records'), db, collection_name_staff)

    elif action == "--get-code-before":
        # Implement code extraction here if needed
        pass

    else:
        print("Invalid action. Use --scrape-and-insert or --get-code-before.")
