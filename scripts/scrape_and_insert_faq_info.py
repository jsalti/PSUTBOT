import os
import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient
import sys

def scrape_faq_info(url):
    # Send a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the container for FAQ items
    faq_container = soup.find('div', class_='faq_body_sec')

    # Extract information about FAQ items
    if faq_container:
        faq_items = faq_container.find_all('div', class_='card')

        faq_data = []
        for item in faq_items:
            question = item.find('h5', class_='faq-title').text.strip()

            # Extracting answers with multiple paragraphs
            answer = '\n'.join([p.text.strip() for p in item.find('div', class_='card-body').find_all('p')])

            faq_data.append({
                "FAQ_Question": question,
                "FAQ_Answer": answer
            })

        return faq_data

    else:
        print("FAQ container not found. Please check the page structure.")
        return None

def save_to_json(data, output_directory, filename):
    # Save the extracted data to a JSON file in the specified directory
    json_file_path = os.path.join(output_directory, filename)
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

    # Print the path to the saved JSON file
    print(f'Data saved to: {json_file_path}')

def insert_faq_to_mongodb(data, db, collection_name):
    # Create a collection
    collection_faq = db[collection_name]

    # Insert JSON data into MongoDB
    collection_faq.insert_many(data)

    print("FAQ data inserted successfully!")

def extract_code_before():
    # Add your code extraction logic here
    print("Code extraction logic goes here.")

if __name__ == "__main__":
    action = sys.argv[1]

    # URLs of the pages you want to scrape
    urls_list = [
        "https://psut.edu.jo/en/faq/faq-category2",
        "https://psut.edu.jo/en/faq/scientific-research",
        "https://psut.edu.jo/en/faq/graduate-studies",
        "https://psut.edu.jo/en/faq/admission-2",
    ]

    # Specify an alternative writable directory (e.g., '/tmp/output_faq')
    output_directory_faq = '/tmp/output_faq'

    # MongoDB Configuration
    mongo_client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
    db = mongo_client['PSUTBOT']

    if action == "--scrape-faq":
        # Collect data for all URLs
        all_faq_data = []
        for i, url in enumerate(urls_list, 1):
            result_faq_data = scrape_faq_info(url)
            if result_faq_data:
                all_faq_data.extend(result_faq_data)

        # Save data to a JSON file
        save_to_json(all_faq_data, output_directory_faq, 'faq_data.json')

        # Insert FAQ data into MongoDB
        collection_name_faq = 'FAQ'
        insert_faq_to_mongodb(all_faq_data, db, collection_name_faq)

    elif action == "--get-code-before":
        # Implement code extraction here if needed
        extract_code_before()

    else:
        print("Invalid action. Use --scrape-faq or --get-code-before.")
