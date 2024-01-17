from pymongo import MongoClient, UpdateOne

# Initialize MongoDB client
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']

def insert_club_information_to_mongodb(data, db, collection_name):
    # Create a collection
    collection = db[collection_name]

    # Convert the dictionary to a list of UpdateOne operations
    operations = [
        UpdateOne(
            {"Club Name": name},
            {"$set": {"Club Description": description}},
            upsert=True
        )
        for name, description in zip(data["Club Name"], data["Description"])
    ]

    # Perform bulk write with upsert
    collection.bulk_write(operations)

    print("Data inserted or updated successfully!")

# Example usage
url_club_information = "https://psut.edu.jo/en/student-life-clubs"
result_club_data = scrape_club_information(url_club_information)

# Check if the result_club_data is not None
if result_club_data is not None:
    collection_name_club = 'Clubs Information'  # Update with your actual collection name
    insert_club_information_to_mongodb(result_club_data, db, collection_name_club)
else:
    print("No data to insert.")
