import os
import requests
import fitz  # PyMuPDF
import json
import time  # Import the time module
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

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

# Set up the WebDriver with Chrome options
chrome_options = Options()
chrome_options.add_argument('--lang=en')
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

# Specify an alternative writable directory
output_directory = '/tmp/output_academic_calendar'
os.makedirs(output_directory, exist_ok=True)

# Specify the absolute path for the PDF file
pdf_file_path = os.path.join(output_directory, 'academic_calendar.pdf')

# Download the PDF
if download_pdf(pdf_url, pdf_file_path):
    # Introduce a delay before accessing the file
    time.sleep(5)  # Adjust the sleep duration as needed

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

# Close the WebDriver when done
driver.quit()
