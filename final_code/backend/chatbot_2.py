from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.schema import AIMessage, HumanMessage
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv
from datetime import datetime as dt
from pymongo import MongoClient

# Initialize MongoDB client
client = MongoClient('mongodb+srv://jana:jr12345@cluster0.2hzth74.mongodb.net/?retryWrites=true&w=majority')
db = client['PSUTBOT']
load_dotenv()

# Initialize OpenAI embeddings and Chroma vector store
openai_embeddings = OpenAIEmbeddings()
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=openai_embeddings)

def generate_personalized_greeting():
    current_hour = dt.now().hour
    if 5 <= current_hour < 12:
        return "Good morning!"
    elif 12 <= current_hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"

def create_psut_prompt(question, chat_history, personalized_greeting):
    # Join previous messages in the chat history to form the context
    context = "\n".join([f"{role}: {content}" for role, content in chat_history])
    print(f"Debug - Context: {context}")
    print(f"Debug - Question: {question}")

    # Create the prompt template
    prompt_template = PromptTemplate(
        input_variables=["question", "context", "personalized_greeting"],
        template=f"""You are PSUTBOT, your friendly PSUT chatbot, here to answer student questions about Princess Sumaya University of Technology. {personalized_greeting}

        Answer the following question based on my knowledge of PSUT and relevant resources: {question}

        Context:
        {context}

        Please ensure that your answers are focused on PSUT and related topics. Here are some examples of questions you can answer:

        1. List all student clubs at PSUT.
        2. Provide information about upcoming events at PSUT.
        3. List the staff members at PSUT along with their emails, phone numbers, office hours and positions.
        4. What are the bachelors and masters programs offered at PSUT?
        5. Share information about the bus schedule, timings, routes, and rounds.
        6. Provide details about the different departments at PSUT.
        7. Answer frequently asked questions.
        8. Share study plans links for various majors.
        9. Answer question related to the dates of the academic calendar 

        Is there anything else you would like to know about PSUT? Feel free to ask any more questions!

        PSUT Quick Links:
        1. [PSUT Official Website](https://www.psut.edu.jo/)
        2. [Instagram](https://www.instagram.com/psutofficial/)
        3. [Facebook](https://www.facebook.com/PSUTOFFICIAL)
        4. [LinkedIn](https://www.linkedin.com/school/princess-sumaya-university-for-technology/)
        5. [YouTube](https://www.youtube.com/@PSUTofficial)
        6. [Twitter](https://twitter.com/PSUTOFFICIAL)

        fun_fact = "PSUT Fun Fact: Princess Sumaya University of Technology was established in 1991."
        PSUT Social Media: Stay connected with PSUT on social media for news and announcements.
        PSUT Motivation: Remember, education is the key to success! Keep striving for excellence.

        PSUT Motto: Empowering minds, shaping the future.

        Chat History:
        {context}
        """
    )

    return prompt_template.format(
        question=question,
        context=context,
        personalized_greeting=personalized_greeting
    )

def ask_ai(question, history=None):
    # Initialize user_id and chat_history list
    user_id = "test102"
    chat_history = []

    # Process history messages within the current session
    if history:
        for message_data in history:
            role = message_data['role']
            content = message_data['content']
            if role == 'assistant':
                chat_history.append(AIMessage(content=content))
            elif role == 'user':
                chat_history.append(HumanMessage(content=content))

    # Append the latest user question to the list
    chat_history.append(HumanMessage(content=question))

    # Initialize ConversationBufferMemory with chat history
    memory = ConversationBufferMemory(memory_key="chat_history", messages=chat_history)

    # Ensure each item in chat_history has exactly two elements (role and content)
    chat_history_strings = [f"{message.role}: {message.content}" for message in chat_history if hasattr(message, 'role') and hasattr(message, 'content')]

    # Join previous messages in the chat history to form the context
    context = "\n".join(chat_history_strings)

    # Create the prompt template
    template = """
    You are PSUTBOT, a friendly chatbot here to answer student questions about Princess Sumaya University of Technology.
    Ensure that your responses are relevant to PSUT and maintain context awareness.

    Please avoid deviating from PSUT-related subjects and provide friendly, informative responses. If you encounter unknown or ambiguous queries, feel free to seek clarification or offer general information about PSUT.

    Chat History:
    {context}

    User Question: {question}

    PSUBOT:
    """

    PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)
    chain = ConversationalRetrievalChain.from_llm(
        llm=OpenAI(model_name="gpt-3.5-turbo", temperature=0.4, streaming=True),
        retriever=vectorstore.as_retriever(search_kwargs={'k': 20}, include_metadata=True),
        memory=memory,
        combine_docs_chain_kwargs={'prompt': PROMPT}
    )

    # Retrieve relevant documents
    docs = vectorstore.similarity_search(question, k=20)

    for idx, doc in enumerate(docs):
        print(f"Document {idx + 1} content: {doc.page_content}")

    kb = docs[0].page_content

    print(f"Fetching data from: {kb}")  # Print the source of data

    # Query ConversationalRetrievalChain
    # Correcting full_query
    full_query = f"""knowledge base: '{kb}' question: '{question}' context: '{context}'"""

    # Query ConversationalRetrievalChain
    response = chain(full_query)

    # Print the retrieved response
    print(f"Retrieved response: {response['answer']}")

    # Return the response
    return {"answer": response["answer"]}

