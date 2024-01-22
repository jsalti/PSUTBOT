from pymongo import MongoClient, UpdateOne
import csv

# Define MongoDB URI
mongo_uri = 'mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority'

def insert_csv_to_mongodb(csv_file_path, database_name, collection_name):
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]

        # Check if the collection exists, if not, MongoDB will create it on the fly
        if collection_name not in db.list_collection_names():
            print(f"Collection {collection_name} does not exist. It will be created.")

        # Open CSV file and prepare a list of UpdateOne operations
        update_operations = []

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Define the filter for the update using the 'study_plans_links' column
                filter_query = {"studyplans_links": row["Major "]}

                # Define the update operation
                update_operation = UpdateOne(
                    filter_query,
                    {
                        "$set": row
                    },
                    upsert=False 
                )

                # Add the update operation to the list
                update_operations.append(update_operation)

        # Perform bulk write with upsert
        result = collection.bulk_write(update_operations)

        print(f"CSV data from {csv_file_path} inserted or updated into MongoDB collection {collection_name} successfully. {result.modified_count} documents modified.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
csv_file_path = '/Users/jinnyy/Desktop/studyplans_links.csv'
insert_csv_to_mongodb(csv_file_path, 'PSUTBOT', 'Study Plans')
