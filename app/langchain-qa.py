# Import necessary modules and libraries
import os, tempfile
import dotenv
import numpy as np
import streamlit as st, pinecone
from langchain.llms.openai import OpenAI
from langchain.vectorstores.pinecone import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader

# Load environment variables
dotenv.load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
pinecone_api_key = os.getenv('PINECONE_API_KEY')
pinecone_env = os.getenv('PINECONE_ENVIRONMENT')
pinecone_index = os.getenv('PINECONE_INDEX_NAME')

st.subheader('Generative Q&A with LangChain & Pinecone')

# Initialize Pinecone and OpenAI
pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

# Create a Pinecone vector database from the existing index
embeddings = OpenAIEmbeddings()
vectordb = Pinecone.from_existing_index(index_name=pinecone_index, embedding=embeddings)

with st.sidebar:
    uploaded_file = st.file_uploader("Upload source document", type="pdf", label_visibility="collapsed")
    if uploaded_file is not None:
        file_list = st.selectbox("Select files", [uploaded_file.name])


# Create a list to store the chat messages
chat_messages = []

# Create a text input field for the user to type their message
query = st.text_input("Type your message here...")

# Create a button for the user to send their message
send_button = st.button("Send")    

# Display the chat messages in a scrollable list
# st.write('\n'.join(chat_messages))



# index = pinecone.Index(pinecone_index)
# query_response = index.query(
#     namespace='example-namespace',
#     top_k=10,
#     include_values=True,
#     include_metadata=True,
#     vector=[0.1, 0.2, 0.3, 0.4],
#     sparseVector={
#         'indices': [10, 45, 16],
#         'values':  [0.5, 0.5, 0.2]
#     },
#     filter={
#         'genre': {'$in': ['physics','class','circuits']}
#     }
# )

# print(query_response)


if send_button:
    print("send button was hit", pinecone_index)
    chat_messages.append(query)
    
    st.markdown('<p style="color:Gray; font-size: 15px;">'+query+'</p>', unsafe_allow_html=True)
    
    # Validate inputs
    if not openai_api_key or not pinecone_api_key or not pinecone_env or not pinecone_index or not query:
        st.warning(f"Please upload the document and provide the missing fields.")
    else:
        try:
            # Save uploaded file temporarily to disk, load and split the file into pages, delete temp file
            # with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            #     tmp_file.write(source_doc.read())
            # loader = PyPDFLoader(tmp_file.name)
            # pages = loader.load_and_split()
            # os.remove(tmp_file.name)
            
            # Generate embeddings for the pages, insert into Pinecone vector database, and expose the index in a retriever interface
            # pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
            # embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
            # vectordb = Pinecone.from_documents(pages, embeddings, index_name=pinecone_index)
            # retriever = vectordb.as_retriever()

            # Initialize the OpenAI module, load and run the Retrieval Q&A chain
            # llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
            # qa = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=retriever)
            # response = qa.run(query)
            

            # Create a retriever from the vector database
            retriever = vectordb.as_retriever()

            # Initialize and run the Retrieval Q&A chain
            qa = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=retriever)
            response = qa.run(query)
            
            st.write(response)
            st.success(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
