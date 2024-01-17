from pymongo import MongoClient, UpdateOne

# Initialize MongoDB client
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']
import pandas as pd
import json

def convert_csv_to_json(csv_file_path, json_file_path):
    """
    Convert a CSV file to JSON.

    Parameters:
        csv_file_path (str): Path to the CSV file.
        json_file_path (str): Path to save the JSON file.
    """
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Convert the DataFrame to JSON (records format)
    json_data = df.to_json(orient='records', lines=True)

    # Specify the output JSON file path
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)

    print(f'Data saved to: {json_file_path}')

