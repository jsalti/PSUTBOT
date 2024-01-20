<p align="center">
  <img src="https://github.com/jsalti/PSUTBOT/assets/104867354/3cc7d7cb-a734-4ac1-9100-bdd97d746f2a" alt="bot_logo" width="400" height="auto">
</p>

# Table of Contents
1. [Description](#description)
2. [Data Loading and Processing](#data-loading-and-processing)
   - [Steps Involved](#steps-involved)
3. [Post-Processing and Model Preparation](#post-processing-and-model-preparation)
   - [Text Splitting](#text-splitting)
   - [Generating Embeddings](#generating-embeddings)
   - [Storing Processed Data](#storing-processed-data)
   - [Data Integration with GPT-3.5](#data-integration-with-gpt-35)
4. [Chatbot Response Generation using GPT-3.5 Turbo](#chatbot-response-generation-using-gpt-35-turbo)
   - [Prompt Templates in LangChain](#prompt-templates-in-langchain)
   - [Conversational Retrieval Chain](#conversational-retrieval-chain)
5. [Conclusion](#conclusion)
# PSUTBOT: The PSUT Chatbot
<!-- ABOUT THE PROJECT -->
## About The Project
PSUTBOT is a university chatbot that would improve student support services by giving immediate, correct answers to their questions. Creating a 
system that could understand the variety of student inquiries, interpret details in the context, and guarantee a user-friendly interface for smooth communication were among the challenges.
In this Git Repository you will learn how to make your own customized chatbot 

## Built With
- [Python](https://www.python.org) - A powerful programming language used for a wide range of applications.
- [Flask](https://flask.palletsprojects.com/) - A lightweight WSGI web application framework in Python.
- [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) - The standard markup language for documents designed to be displayed in a web browser.
- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) - Cascading Style Sheets used for styling web pages.
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) - A scripting language for creating dynamic web content.
- [Jenkins](https://www.jenkins.io) - An open-source automation server used for continuous integration and delivery.
- [MongoDB](https://www.mongodb.com) - A NoSQL database program, using JSON-like documents with optional schemas.
 
<!-- GETTING STARTED -->
## Getting Started
### Prerequisites
* install python
  ```sh
    https://www.python.org/downloads/
  ```
* install Jenkins 
  ```sh
   https://www.jenkins.io/download/
  ``` 
* install Mongodb
  ```sh
      https://www.mongodb.com/try/download/community
  ```
* Getting API key by OpenAI
  ```sh
     https://openai.com/
  ```
* install project requirements 
  ```sh
     pip install -r requirements.txt
  ```
  
## Data Loading and Processing

This section outlines the process of extracting data from the official website of PSUT (Princess Sumaya University for Technology), and how it is subsequently processed and stored in a MongoDB database.

### Steps Involved

1. **Data Extraction**: 
   - The data was extracted from the [official website of PSUT](https://www.psut.edu.jo/).
   - Utilized web scraping techniques to programmatically gather the required data.
   - some of the data was collected manually (e.g. office hours for the doctors in psut ,bus schedule )
2. **Data Preprocessing**:
   Before inserting the data into MongoDB, the following preprocessing steps were performed:
   - **Restructuring the Data**: The raw data was restructured into a more manageable and usable format. This involved organizing the data into coherent sets that align with our database .
   - **Standardizing Field Text**: Ensured that all text fields in the data are standardized for consistency. This includes formatting dates, normalizing text entries, and correcting any inconsistencies found in the raw data.

3. **Inserting Data into MongoDB**:
   - Established a connection to our MongoDB database.
   - Inserted the processed data into the database, ensuring that it conforms to the defined schema.
4. **Automation with Jenkins**:
   - The entire process of data extraction,and insertion into MongoDB is automated using Jenkins.
   - Jenkins jobs are configured to periodically run the data pipeline, ensuring that the latest data is always captured and processed.
   - This automation enhances the efficiency and reliability of the data management process.

### Tools and Libraries Used
- Web scraping libraries (e.g., BeautifulSoup, Scrapy)
- Data processing libraries in Python (e.g., pandas,json,csv)
- MongoDB as the database for storing processed data
- Jenkins for automating the data pipeline.
### Note
- Ensure that web scraping is done in compliance with the website's terms of service and privacy policy.
- Sensitive data should be handled and stored securely, adhering to data protection regulations.

  
### Post-Processing and Model Preparation
After inserting the data into MongoDB, further processing is performed to prepare the data for our GPT-3.5 turbo model. This involves text splitting and generating embeddings.

### Steps Involved

1. **Text Splitting**:
   - We use the `langchain.text_splitter.RecursiveCharacterTextSplitter` from the Langchain library to split the data into manageable chunks.
   - This is necessary to ensure the data fits within the text limits of the GPT-3.5 turbo model and to facilitate more efficient processing.

2. **Generating Embeddings**:
   - With the data now in smaller chunks, we proceed to generate embeddings.
   - For this, we use OpenAI's API, utilizing an API key provided by OpenAI.which can be obtained from [OpenAI](https://openai.com/).
   - The embeddings are created to transform the text data into a format that is more suitable for machine learning models, specifically the GPT-3.5 turbo model.

3. **Storing Processed Data**:
   - After generating the embeddings, this processed data is stored in a vector store called Chroma, provided by `langchain.vectorstores`.
   - To implement this, we use the `Chroma` class from the `langchain.vectorstores` package.
   - The data, now with generated embeddings, is stored in Chroma, making it efficiently accessible for retrieval and use by our GPT-3.5 turbo model.

4. **Data Integration with GPT-3.5**:
   - The embeddings stored in Chroma are integrated with the GPT-3.5 turbo model.
   - This integration enables the model to leverage the processed data for various NLP tasks, enhancing its performance and accuracy.

### Important Notes

- Ensure all steps are followed in sequence for optimal data preparation and integration with the GPT-3.5 turbo model.
- Handle the data and embeddings with care to maintain integrity and context.

### Tools and Libraries Used

- MongoDB for initial data storage.
- Text splitting library .
- OpenAI API for generating embeddings.
- Chroma from `langchain.vectorstores` for storing processed embeddings.
- GPT-3.5 turbo model for advanced natural language processing tasks.

### Chatbot Response Generation using GPT-3.5 Turbo

#### Prompt Templates in LangChain

- Customized interaction framework using `PromptTemplate`.
- Focused on PSUT-related inquiries and provided quick links and resources.

#### Example Prompt Template

```python
template = '''
You are PSUTBOT, your friendly PSUT chatbot, here to answer student questions about Princess Sumaya University of Technology. {personalized_greeting}

[Additional template content]
'''
prompt_template = PromptTemplate(
    input_variables=["question", "context", "personalized_greeting"],
    template=template
)
```

#### Conversational Retrieval Chain

- Implemented `ConversationalRetrievalChain` from LangChain.
- Used `ConversationBufferMemory` for context awareness.

## Conclusion

PSUTBOT delivers a highly engaging and informative conversational experience, tailored to the PSUT community, leveraging advanced technologies like GPT-3.5 Turbo and LangChain.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


