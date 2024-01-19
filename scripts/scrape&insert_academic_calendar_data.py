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
from pymongo import MongoClient
import sys

def download_pdf(pdf_url, destination_path):
    try:
        response = requests.get(pdf_url)
        with open(destination_path, 'wb') as pdf_file:
            pdf_file.write(response.content)
        return True
    except Exception as e:
        print(f"Error downloading PDF: {e}")
        return False

def extract_pdf_text(pdf_path):
    try:
        pdf_document = fitz.open(pdf_path)
        text_data = []
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text_data.append(page.get_text())
        pdf_document.close()
        return text_data
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def scrape_academic_calendar(url, output_directory):
    # Set up the WebDriver with Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--lang=en')
    chromedriver_autoinstaller.install()

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the specified URL
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

    # Specify the absolute path for the PDF file
    pdf_file_path = os.path.join(output_directory, 'academic_calendar.pdf')

    # Download the PDF
    if download_pdf(pdf_url, pdf_file_path):
        # Extract text from the PDF
        text_data = extract_pdf_text(pdf_file_path)

        if text_data is not None:
            # Save the extracted text to a JSON file in the specified directory
            json_file_path = os.path.join(output_directory, 'academic_calendar_text.json')
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump({"Text": text_data}, json_file, ensure_ascii=False, indent=2)

            # Print the path to the saved JSON file
            print(f'Text saved to: {json_file_path}')

            # Combine all text data into one table
            combined_table = ' '.join(text_data)

            # Print the combined table
            print(f'Combined Table:\n{combined_table}\n{"-" * 50}')

            return combined_table

    # Close the WebDriver when done
    driver.quit()

def insert_into_mongodb(data, db_uri, db_name, collection_name):
    # MongoDB Configuration
    mongo_client = MongoClient(db_uri)
    db = mongo_client[db_name]
    collection = db[collection_name]

    # Update existing document or insert a new one based on 'academic_calendar_id' field
    filter_criteria = {"academic_calendar_id": "some_unique_identifier"}
    update_data = {"$set": {"academic_calendar_information": data, "academic_calendar_id": "some_unique_identifier"}}
    collection.update_many(filter_criteria, update_data, upsert=True)

    print('Data inserted or updated successfully into MongoDB')

if __name__ == "__main__":
    action = sys.argv[1]

    # URL and output directory for academic calendar data
    academic_calendar_url = 'https://psut.edu.jo/'
    academic_calendar_output_directory = '/tmp/output_academic_calendar'

    if action == "--scrape-academic-calendar":
        data = scrape_academic_calendar(academic_calendar_url, academic_calendar_output_directory)
        if data:
            insert_into_mongodb(data, 'mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority', 'PSUTBOT', 'Academic Calendar')
    else:
        print("Invalid action. Use --scrape-academic-calendar.")
