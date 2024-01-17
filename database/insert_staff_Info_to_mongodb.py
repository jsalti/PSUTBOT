from pymongo import MongoClient, UpdateOne

# Initialize MongoDB client
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']

def insert_data_into_mongodb(data_list, collection):
    # MongoDB insertion
    collection.insert_many(data_list)
    print(f"Data inserted successfully into MongoDB!")

def scrape_all_staff_info_and_insert_into_mongodb(base_url, collection):
    total_pages = get_total_pages(base_url)
    staff_info_list = []

    for page_number in range(total_pages, 0, -1):
        url = base_url.format(page_number)
        print(f"Processing page {page_number}: {url}")

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        staff_links = soup.find_all('a', href=lambda href: href and '/en/staff/professor/' in href)

        for staff_link in staff_links:
            staff_url = f"https://www.psut.edu.jo{staff_link['href']}"

            # Check if the staff URL is already processed
            if staff_url not in [info['Individual Page'] for info in staff_info_list]:
                staff_info = extract_staff_info(staff_url)

                if staff_info:
                    staff_info_list.append(staff_info)

    # Insert data into MongoDB
    insert_data_into_mongodb(staff_info_list, collection)

# URL pattern for the staff pages
base_url = "https://www.psut.edu.jo/en/staff/professor?page={}"

# MongoDB connection details
collection_name = "staff_info_collection"
collection = db[collection_name]

# Scrape all staff information and insert into MongoDB
scrape_all_staff_info_and_insert_into_mongodb(base_url, collection)
