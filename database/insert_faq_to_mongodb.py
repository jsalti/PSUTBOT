from pymongo import MongoClient, UpdateOne


# Initialize MongoDB client
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']

def insert_faq_to_mongodb(data, db, collection_name):
    """
    Inserts or updates FAQ data into MongoDB.

    Parameters:
        data (list): List of dictionaries containing FAQ data.
        db: MongoDB database object.
        collection_name (str): Name of the collection to insert data into.
    """
    # Create a collection
    collection = db[collection_name]

    # Update or insert data into MongoDB using UpdateOne with upsert
    operations = [UpdateOne(
        {"FAQ Question": item["FAQ Question"]},
        {"$set": item},
        upsert=True
    ) for item in data]

    collection.bulk_write(operations)
    print("FAQ data inserted or updated successfully into MongoDB!")


# URLs of the pages you want to scrape
urls_list = [
    "https://psut.edu.jo/en/faq/faq-category2",
    "https://psut.edu.jo/en/faq/scientific-research",
    "https://psut.edu.jo/en/faq/graduate-studies",
    "https://psut.edu.jo/en/faq/admission-2",
]

# Collect data for all URLs
all_faq_data = []
for url in urls_list:
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
collection_name_faq = 'FAQ'  # Update with your actual collection name

# Call the function to insert or update data into MongoDB
insert_faq_to_mongodb(all_faq_data, db, collection_name_faq)

print("FAQ data inserted or updated successfully into MongoDB!")
