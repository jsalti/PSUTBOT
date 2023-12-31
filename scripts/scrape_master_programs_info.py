# -*- coding: utf-8 -*-
"""scrape_master_programs_info.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AxOyh0eS0ezGHIfJtpYpcTbZMH5thcC0
"""

import os
import requests
from bs4 import BeautifulSoup
import json

def scrape_master_programs_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses
        html_content = response.text

        # Parse the HTML content using BeautifulSoup
        soup_master_programs = BeautifulSoup(html_content, "html.parser")

        # Find the container for the program information
        program_container = soup_master_programs.find("div", class_="tab-pane fade show active")

        # Extract information about programs
        programs = program_container.find_all("a", href=True)

        program_data = []
        for program in programs:
            name_tag = program.find("h4")
            description_tag = program.find("p")

            if name_tag and description_tag:
                program_name = name_tag.text.strip()
                program_description = description_tag.text.strip()
                program_link = program.get("href")

                program_data.append({
                    "Program Name": program_name,
                    "Description": program_description,
                    "Link": program_link
                })

        return program_data
    except Exception as e:
        print(f"Error scraping master's programs: {e}")
        return None

# Example URL
url_master_programs = "https://psut.edu.jo/en/school/School_of_Graduate_Studies_Scientific_Research"

# Call the function to scrape master's programs information
master_programs_data = scrape_master_programs_from_url(url_master_programs)

if master_programs_data is not None:
    # Specify the directory where you have write permissions
    output_directory = '/tmp/output_masters'

    # Ensure the directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Specify the output JSON file path
    output_json_file = os.path.join(output_directory, 'master_programs_data.json')

    # Save the extracted data to a JSON file
    with open(output_json_file, 'w', encoding='utf-8') as json_file:
        json.dump(master_programs_data, json_file, ensure_ascii=False, indent=2)

    print(f'Data saved to: {output_json_file}')
else:
    print("No data to save.")
