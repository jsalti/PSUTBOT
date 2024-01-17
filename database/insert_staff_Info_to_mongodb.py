from pymongo import MongoClient, UpdateOne
from scrape_staff_info import scrape_all_staff_info(base_url), get_total_pages(base_url)

# Initialize MongoDB client
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']

from pymongo import MongoClient

# Insert data into MongoDB
def insert_staff_info_to_mongodb(data, db, collection_name):
    
    collection = db[collection_name]
    collection.insert_many(data.to_dict(orient='records'))
    print("Data inserted into MongoDB!")

# Example usage
collection_name = 'Staff Information'  # Update with your actual collection name
insert_staff_info_to_mongodb(result_staff_info, 'PSUTBOT', collection_name)
