from pymongo import MongoClient, UpdateOne
import csv

# Initialize MongoDB client
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']

def read_bus_schedule_csv(csv_file_path):
    # Open the CSV file
    with open(csv_file_path, 'r') as csvfile:
        # Read the CSV file
        reader = csv.DictReader(csvfile)

        # Initialize the dictionary
        routes_data = {}

        # Iterate over the rows in the CSV file
        for row in reader:
            # Extract the route name
            route_name = row["Route "]

            # If the route is not already in the dictionary, add it with an empty list as its value
            if route_name not in routes_data:
                routes_data[route_name] = []

            # Extract timings for each round
            timings = {round_name: time for round_name, time in row.items() if round_name != "Route"}

            # Add the timings to the list for the current route
            routes_data[route_name].append({
                "timings": timings
            })

    return routes_data

def insert_bus_schedule_into_mongodb(routes_data):
    # Connect to MongoDB
    collection = db["Bus_Schedule"]

    # Create a list of UpdateOne operations for bulk write
    update_operations = [
        UpdateOne(
            {"route_name": route_name},
            {"$addToSet": {"rounds": {"$each": round_data["timings"]}}},
            upsert=True
        )
        for route_name, round_list in routes_data.items() for round_data in round_list
    ]

    # Perform bulk write with upsert
    collection.bulk_write(update_operations)

# Example usage:
csv_file_path = "/Users/jinnyy/Desktop/BusSchedule.csv"
routes_data = read_bus_schedule_csv(csv_file_path)

# Print the routes_data dictionary
for route_name, round_list in routes_data.items():
    for round_data in round_list:
        print(f"{route_name}: {round_data}")

# Insert data into MongoDB using UpdateOne
insert_bus_schedule_into_mongodb(routes_data)
