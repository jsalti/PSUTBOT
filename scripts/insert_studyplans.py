from pymongo import MongoClient, UpdateOne
import csv

# Define MongoDB URI
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']

def read_study_plans_csv(csv_file_path):
    # Open the CSV file
    with open(csv_file_path, 'r') as csvfile:
        # Read the CSV file
        reader = csv.DictReader(csvfile)

        # Initialize the dictionary
        study_plans_data = {}

        # Iterate over the rows in the CSV file
        for row in reader:
            # Extract the major name
            major_name = row["Major"]

            # If the major is not already in the dictionary, add it with an empty list as its value
            if major_name not in study_plans_data:
                study_plans_data[major_name] = []

            # Extract the link to the study plan
            study_plan_link = row["link to study plan"]

            # Add the link to the list for the current major
            study_plans_data[major_name].append({
                "study_plan_link": study_plan_link
            })

    return study_plans_data

def insert_study_plans_into_mongodb(study_plans_data):
    # Connect to MongoDB
    collection = db["Study_Plans"]

    # Create a list of UpdateOne operations for bulk write
    update_operations = [
        UpdateOne(
            {"major_name": major_name},
            {"$addToSet": {"study_plans": {"$each": major_data["study_plan_link"]}}},
            upsert=True
        )
        for major_name, major_list in study_plans_data.items() for major_data in major_list
    ]

    # Perform bulk write with upsert
    collection.bulk_write(update_operations)

# Example usage:
csv_file_path = '/Users/jinnyy/Desktop/studyplans_links.csv'
study_plans_data = read_study_plans_csv(csv_file_path)

# Print the study_plans_data dictionary
for major_name, major_list in study_plans_data.items():
    for major_data in major_list:
        print(f"{major_name}: {major_data}")

# Insert data into MongoDB using UpdateOne
insert_study_plans_into_mongodb(study_plans_data)
