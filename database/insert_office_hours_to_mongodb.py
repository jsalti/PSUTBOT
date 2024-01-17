from pymongo import MongoClient, UpdateOne

# Initialize MongoDB client
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']

import csv

def read_office_hours_csv(csv_file_path):
    # Open the CSV file
    with open(csv_file_path, 'r') as csvfile:
        # Read the CSV file
        reader = csv.reader(csvfile)

        # Initialize the dictionary
        doctor_hours = {}

        # Iterate over the rows in the CSV file
        for row in reader:
            # Extract the doctor name, day, and time range
            doctor_name, day, *time_range = row

            # If the doctor is not already in the dictionary, add them with an empty list as their value
            if doctor_name not in doctor_hours:
                doctor_hours[doctor_name] = []

            # Add the day and time range directly to the list for the current doctor
            # If "no office hours" or "by appointment" is present, only write it once for each day
            if "no office hours" in time_range or "by appointment" in time_range:
                # Check if the current day is "no office hours" and write it only once
                if "no office hours" in day:
                    doctor_hours[doctor_name].append(f"has no office hours on {day} {' '.join(time_range)}")
                else:
                    doctor_hours[doctor_name].append(f"has office hours on {day} from {' '.join(sorted(set(time_range)))}")  # Use sorted to ensure correct order
            else:
                doctor_hours[doctor_name].append(f"has office hours on {day} from {' '.join(sorted(set(time_range)))}")  # Use sorted to ensure correct order

    return doctor_hours

def insert_into_mongodb(doctor_hours):
    # Connect to MongoDB
    collection = db["Office_Hours"]

    # Create a list of UpdateOne operations for bulk write
    update_operations = [
        UpdateOne(
            {"doctor_name": doctor_name},
            {"$addToSet": {"office_hours": {"$each": hours_list}}},
            upsert=True
        )
        for doctor_name, hours_list in doctor_hours.items()
    ]

    # Perform bulk write with upsert
    collection.bulk_write(update_operations)

# Example usage:
csv_file_path = "/Users/jinnyy/Desktop/Office hours.csv"
doctor_hours = read_office_hours_csv(csv_file_path)

# Print the doctor_hours dictionary
for doctor_name, hours_list in doctor_hours.items():
    print(f"{doctor_name}: {', '.join(hours_list)}")

# Insert data into MongoDB using UpdateOne
insert_into_mongodb(doctor_hours)
