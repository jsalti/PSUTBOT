import csv
import json
from pymongo import MongoClient, UpdateOne
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']
def csv_to_dict(csv_file):
    routes_dict = {}
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row
        rounds = header[1:]

        for row in reader:
            route_name = row[0]
            timings = {round_name: time for round_name, time in zip(rounds, row[1:])}
            routes_dict[route_name] = timings

    return routes_dict

def save_to_json(data, json_file):
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=2)

def insert_csv_to_mongodb(csv_file_path, database_name, collection_name, mongo_uri):
    # Connect to MongoDB
    collection = db["Bus Schedule"]

    # Open CSV file and prepare a list of UpdateOne operations
    update_operations = []

    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Define the filter for the update using the 'Route Name' column
            filter_query = {"Route": row["Route "]}

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

    # Print debug information
    print("Filter Query:", filter_query)
    print("Update Operations:", update_operations)

    # Perform bulk write with upsert
    try:
        collection.bulk_write(update_operations)
        print(f"CSV data from {csv_file_path} inserted or updated into MongoDB collection {collection_name} successfully.")
    except Exception as e:
        print(f"Error during bulk write: {e}")

# Example usage
csv_file_path = "/Users/jinnyy/Desktop/BusSchedule.csv"
json_file_path = 'output_routes.json'
mongo_uri = 'mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority'

routes_data = csv_to_dict(csv_file_path)
save_to_json(routes_data, json_file_path)
insert_csv_to_mongodb(csv_file_path, 'PSUTBOT', 'Bus Schedule', mongo_uri)
