# -*- coding: utf-8 -*-
"""extract_academic_calendar_data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NvBc6cAV3xL-s-5DEwyPbD62RwAwNeX8
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
import fitz  # PyMuPDF
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

def extract_calandar_data(pdf_url):
    # Download the PDF
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

    # Return the extracted text data
    return data

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
data = extract_calandar_data(pdf_url)

# Close the WebDriver when done
driver.quit()

# Specify an alternative writable directory
output_directory = '/tmp/output_academic_calendar'
os.makedirs(output_directory, exist_ok=True)

# Save the extracted data to a JSON file in the specified directory
json_file_path = os.path.join(output_directory, 'extracted_data.json')
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=2)

# Print the path to the saved JSON file
print(f'Data saved to: {json_file_path}')