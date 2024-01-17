from pymongo import MongoClient, UpdateOne

# Initialize MongoDB client
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']

def insert_office_hours_to_mongodb(json_file_path, db, collection_name):
    """
    Insert JSON data into MongoDB.

    Parameters:
        json_file_path (str): Path to the JSON file.
        db: MongoDB database object.
        collection_name (str): Name of the collection to insert data into.
    """
    # Create a collection
    collection_off_hr = db['office_hours']

    # Load the JSON data from the file and insert each line separately into MongoDB
    with open(json_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            json_data = json.loads(line)

            # Insert JSON data into MongoDB
            collection.insert_one(json_data)

    print("Data inserted successfully into MongoDB!")

# Example usage
csv_file_path = r'C:\Users\BASIL\Desktop\Office hours.csv'
json_file_path = r'C:\Users\BASIL\Desktop\Office_hours.json'
collection_name_off_hr = 'office_hours'  # Update with your actual collection name

# Convert CSV to JSON
convert_csv_to_json(csv_file_path, json_file_path)

# Insert JSON data into MongoDB
insert_office_hours_to_mongodb(json_file_path, db, collection_name_off_hr)

