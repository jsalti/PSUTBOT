from pymongo import MongoClient, UpdateOne

# Initialize MongoDB client
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']

def insert_school_info_to_mongodb(data, db, collection_name):
    """
    Inserts school information into MongoDB.

    Parameters:
        data (dict): School information data dictionary.
        db: MongoDB database object.
        collection_name (str): Name of the collection to insert data into.
    """
    # Create a collection

    collection_school_info = db['school information']

    # Insert JSON data into MongoDB
    collection_school_info.insert_one(data)

    print("Data inserted successfully!")

# Example usage

collection_name_school = 'school_information'  # Update with your actual collection name

# Load the JSON data from the file
with open(json_file_path_all_data, 'r', encoding='utf-8') as file:
    all_data = json.load(file)

# Iterate over each URL's data and insert into MongoDB
for url, data_for_url in all_data.items():
    print(f"Inserting data for URL: {url}")
    # Call the function to insert data into MongoDB
    insert_school_info_to_mongodb(data_for_url, db, collection_name_school)

print("All data inserted successfully into MongoDB!")
