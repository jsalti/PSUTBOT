import os
import requests
from bs4 import BeautifulSoup
import json

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
                " FAQ_Question": question,
                "FAQ_Answer": answer
            })

        return faq_data

    else:
        print("FAQ container not found. Please check the page structure.")
        return None

# URLs of the pages you want to scrape
urls_list = [
    "https://psut.edu.jo/en/faq/faq-category2",
    "https://psut.edu.jo/en/faq/scientific-research",
    "https://psut.edu.jo/en/faq/graduate-studies",
    "https://psut.edu.jo/en/faq/admission-2",
]

# Collect data for all URLs
all_faq_data = []
for i, url in enumerate(urls_list, 1):
    result_faq_data = scrape_faq_info(url)
    if result_faq_data:
        all_faq_data.extend(result_faq_data)

# Specify an alternative writable directory (e.g., '/tmp/output_faq')
output_directory_faq = '/tmp/output_faq'

# Create the output directory if it doesn't exist
os.makedirs(output_directory_faq, exist_ok=True)

# Save the extracted data to a JSON file in the specified directory
json_file_path = os.path.join(output_directory_faq, 'faq_data.json')

with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_faq_data, json_file, ensure_ascii=False, indent=2)

# Print the path to the saved JSON file
print(f'Data saved to: {json_file_path}')


def insert_faq_to_mongodb(data, db, collection_name):
    """
    Inserts FAQ data into MongoDB.

    Parameters:
        data (list): List of dictionaries containing FAQ data.
        db: MongoDB database object.
        collection_name (str): Name of the collection to insert data into.
    """
    # Create a collection
    collection_faq = db[collection_name]

    # Insert JSON data into MongoDB
    collection_faq.insert_many(data)

    print("FAQ data inserted successfully!")

# URLs of the pages you want to scrape
urls_list = [
    "https://psut.edu.jo/en/faq/faq-category2",
    "https://psut.edu.jo/en/faq/scientific-research",
    "https://psut.edu.jo/en/faq/graduate-studies",
    "https://psut.edu.jo/en/faq/admission-2",
]

# Collect data for all URLs
all_faq_data = []
for i, url in enumerate(urls_list, 1):
    result_faq_data = scrape_faq_info(url)
    if result_faq_data:
        all_faq_data.extend(result_faq_data)

# Specify an alternative writable directory (e.g., '/tmp/output_faq')
output_directory_faq = '/tmp/output_faq'

# Create the output directory if it doesn't exist
os.makedirs(output_directory_faq, exist_ok=True)

# Save the extracted data to a JSON file in the specified directory
json_file_path = os.path.join(output_directory_faq, 'faq_data.json')

with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_faq_data, json_file, ensure_ascii=False, indent=2)

# Print the path to the saved JSON file
print(f'Data saved to: {json_file_path}')

# Insert FAQ data into MongoDB using the function
collection_name_faq = 'faq_information'  # Update with your actual collection name

# Load the JSON data from the file as a list
with open(json_file_path, 'r', encoding='utf-8') as file:
    faq_data_list = json.load(file)

# Call the function to insert data into MongoDB
insert_faq_to_mongodb(faq_data_list, db, collection_name_faq)

print("FAQ data inserted successfully into MongoDB!")
