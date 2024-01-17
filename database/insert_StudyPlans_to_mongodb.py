from pymongo import MongoClient, UpdateOne
import csv

def insert_csv_to_mongodb(csv_file_path, database_name, collection_name, mongo_uri):
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client[database_name]
    collection = db[collection_name]

    # Open CSV file and prepare a list of UpdateOne operations
    update_operations = []

    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Define the filter for the update using the 'study_plans_links' column
            filter_query = {"study_plans_links": row["study_plans_links"]}

            # Define the update operation
            update_operation = UpdateOne(
                filter_query,
                {
                    "$set": row
                },
                upsert=True
            )

            # Add the update operation to the list
            update_operations.append(update_operation)

    # Perform bulk write with upsert
    collection.bulk_write(update_operations)

    print(f"CSV data from {csv_file_path} inserted or updated into MongoDB collection {collection_name} successfully.")

# Example usage
csv_file_path = '/Users/jinnyy/Desktop/study_plans_links.csv'
mongo_uri = 'mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority'
insert_csv_to_mongodb(csv_file_path, 'PSUTBOT', 'Study Plans', mongo_uri)
