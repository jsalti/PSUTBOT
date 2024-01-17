from pymongo import MongoClient, UpdateOne

# Initialize MongoDB client
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']

import requests
import os
import fitz  # PyMuPDF
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import pymongo

def extract_calendar_data(pdf_url):
    response = requests.get(pdf_url)

    # Create a "static/" directory in the current working directory
    static_directory = os.path.join(os.getcwd(), 'static')
    os.makedirs(static_directory, exist_ok=True)

    # Specify the absolute path for the PDF file
    pdf_file_path = os.path.join(static_directory, 'academic_calendar.pdf')
    with open(pdf_file_path, 'wb') as pdf_file:
        pdf_file.write(response.content)

    # Use PyMuPDF to extract text from the PDF
    pdf_document = fitz.open(pdf_file_path)
    data = []
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        lines = page.get_text("text").splitlines()
        formatted_text = ' '.join(lines)
        data.append(formatted_text)

    # Close the PDF document
    pdf_document.close()

    return data

def insert_data_to_mongodb(db, collection_name, data):
    collection = db[collection_name]
    collection.insert_one({"academic_calendar_data": data})
    print("Data inserted successfully into MongoDB!")

# Set up the WebDriver with Chrome options
chrome_options = Options()
chrome_options.add_argument('--lang=en')

# Use chromedriver_autoinstaller to ensure the latest Chromedriver is installed
chromedriver_autoinstaller.install()

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the main URL
url = 'https://psut.edu.jo/'
driver.get(url)

# Wait for the "Academic Calendar" button to be clickable
academic_calendar_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div/div[1]/a/span'))
)

# Click on the "Academic Calendar" button
academic_calendar_button.click()

# Wait for the second button inside the Academic Calendar page to be clickable
second_button_xpath = '//*[@id="readspeakerDiv"]/div/div/div[2]/div/div[2]/h2[2]/a'
second_button = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, second_button_xpath))
)

# Get the PDF URL from the second button's href attribute
pdf_url = second_button.get_attribute('href')

# Extract data from the PDF
data = extract_calendar_data(pdf_url)

# Close the WebDriver when done
driver.quit()


# Specify the collection name
collection_name = 'academic_calendar'

# Insert data into MongoDB using the function
insert_data_to_mongodb(db, collection_name, data)
