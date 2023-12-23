# -*- coding: utf-8 -*-
"""scrape_student_life_activities.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fiQFqTopF8_FmxcU7lZbdHZIgAcZ1TgS
"""

import os
import requests
import fitz  # PyMuPDF
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time
import json

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