from pymongo import MongoClient, UpdateOne
from pymongo import MongoClient, UpdateOne
from scrape_student_life_activities import scrape_student_life_activities

# Initialize MongoDB client
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']

def insert_student_life_activities_to_mongodb(data, db, collection_name):
    # Create a collection
    collection_event = db[collection_name]

    # Convert the dictionary to a list of UpdateOne operations
    operations = [
        UpdateOne(
            {"Event Name": name},
            {"$set": {"Event Description": description}},
            upsert=True
        )
        for name, description in zip(data["event_name"], data["event_description"])
    ]

    # Perform bulk write with upsert
    collection_event.bulk_write(operations)

    print("Data inserted or updated successfully!")

# Example usage
url_student_life_activities = "https://psut.edu.jo/en/student-life-activities"
result_event_data = scrape_student_life_activities(url_student_life_activities)

# Check if the result_event_data is not None
if result_event_data is not None:
    collection_name_events = 'Events'  # Update with your actual collection name
    insert_student_life_activities_to_mongodb(result_event_data, db, collection_name_events)
else:
    print("No data to insert.")
