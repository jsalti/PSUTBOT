
import os
import requests
from bs4 import BeautifulSoup
import json

def scrape_student_life_activities(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the relevant HTML elements containing the event/activity information
        event_elements = soup.find_all("div", class_="col-md-6 col-lg-3")

        # Create lists to store event information
        event_names = []
        event_descriptions = []

        # Extract information and populate lists
        for event in event_elements:
            event_name = event.find("h5").find("a").text.strip()
            event_description = event.find("p").text.strip()

            event_names.append(event_name)
            event_descriptions.append(event_description)

        # Create a dictionary from the lists
        data = {
            "event_name": event_names,
            "event_description": event_descriptions
        }

        return data  # Return the data dictionary

    else:
        print("Failed to retrieve the page.")
        return None

# URL of the page you want to scrape
url_student_life_activities = "https://psut.edu.jo/en/student-life-activities"

result_event_data = scrape_student_life_activities(url_student_life_activities)

# Check if the result_event_data is not None before saving to a JSON file
if result_event_data is not None:
    output_directory_event = '/tmp/output_event'

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory_event, exist_ok=True)

    # Save the extracted data to a JSON file in the specified directory
    json_file_path_event = os.path.join(output_directory_event, 'student_life_activities.json')
    with open(json_file_path_event, 'w', encoding='utf-8') as json_file_event:
        json.dump(result_event_data, json_file_event, ensure_ascii=False, indent=2)

    # Print the path to the saved JSON file
    print(f'Data saved to: {json_file_path_event}')
else:
    print("No data to save.")


def insert_student_life_activities_to_mongodb(data, db, collection_name):
    """
    Inserts student life activities information into MongoDB.

    Parameters:
        data (dict): Student life activities information data dictionary.
        db: MongoDB database object.
        collection_name (str): Name of the collection to insert data into.
    """
    # Create a collection
    collection_event = db['Events']

    # Convert the dictionary to a list of documents
    documents = [{"event_name": name, "event_description": description} for name, description in zip(data["event_name"], data["event_description"])]

    # Insert JSON data into MongoDB
    collection_event.insert_many(documents)

    print("Data inserted successfully!")

# Example usage
url_student_life_activities = "https://psut.edu.jo/en/student-life-activities"
result_event_data = scrape_student_life_activities(url_student_life_activities)

# Check if the result_event_data is not None
if result_event_data is not None:
    collection_name_events = 'student_life_activities'  # Update with your actual collection name
    insert_student_life_activities_to_mongodb(result_event_data, db, collection_name_events)
else:
    print("No data to insert.")
