from pymongo import MongoClient, UpdateOne

# Initialize MongoDB client
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']

from pymongo import MongoClient, UpdateOne
import json
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to get the total number of pages
def get_total_pages(base_url):
    url = base_url.format(1)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    last_page = soup.find('a', class_='page-link', string='9')

    if not last_page:
        last_page = soup.find('a', class_='page-link', string=lambda s: s and s.isdigit())

    total_pages = int(last_page['data-page']) if last_page else 1
    return total_pages

# Function to extract staff information from a single staff page
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

# Function to insert staff information into MongoDB
def insert_staff_info_to_mongodb(staff_info, db, collection_name):
    # Create a collection
    collection = db[collection_name]

    # Convert the staff information to an UpdateOne operation
    filter_condition = {"Name": staff_info["Name"]}
    update_operation = UpdateOne(
        filter_condition,
        {"$set": staff_info},
        upsert=True
    )

    # Perform the update operation
    collection.bulk_write([update_operation])

    print(f"Staff information for {staff_info['Name']} inserted or updated successfully!")

# Function to scrape staff information from all pages and save it to MongoDB
def scrape_and_insert_staff_info(base_url, db, collection_name):
    total_pages = get_total_pages(base_url)

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
                insert_staff_info_to_mongodb(staff_info, db, collection_name)

# URL pattern for the staff pages
base_url = "https://www.psut.edu.jo/en/staff/professor?page={}"


# Collection name in MongoDB
collection_name_staff = 'Staff Information'  # Update with your actual collection name

# Scrape staff information and insert into MongoDB
scrape_and_insert_staff_info(base_url, db, collection_name_staff)

