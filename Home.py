import streamlit as st
import random
import time
from InputParsing import ChatClass
from Ingest import SendDocToPineCone

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'api_keys_validated' not in st.session_state:
    st.session_state['api_keys_validated'] = False
if 'file_uploaded' not in st.session_state:
    st.session_state['file_uploaded'] = False

# Function Definitions for Each Page
def home_page():
    st.markdown(
    """
    Welcome to **Document GPT** demo! This app lets you upload documents and use the convinient chat function to \
    ask questions about the document. The model will generate a question based on the document and the question \
    To Use this app, please follow the steps below: \n \n

    1. Verify the OpenAI Key 
    2. Upload the Document 
    3. Get Chatting! \n \n
"""
)
    if st.button('Get Started'):
        st.session_state['page'] = 'api_key_input'

def submit_key(oKey, pKey):
    st.session_state['openaikey'] = oKey
    st.session_state['pineconekey'] = pKey


def api_key_input_page():
    openai_key = st.text_input("Enter your OpenAI API Key")
    pinecone_key = st.text_input("Enter your Pinecone API Key")

    
    if st.button('Verify API Keys'):
        submit_key(openai_key, pinecone_key)
        # TODO: Add your logic for API key validation here
        # If validation is successful:
        st.session_state['api_keys_validated'] = True
        st.session_state['page'] = 'document_upload'

def document_upload_page():
    uploaded_files = st.file_uploader("Upload documents", accept_multiple_files=True)
    if st.button('Upload'):
        sendDocToPineCone = SendDocToPineCone(st.session_state['pineconekey'], st.session_state['openaikey'])
        for uploaded_file in uploaded_files:
            # TODO: Process each uploaded file as needed
            sendDocToPineCone.uploadtoPineCone(uploaded_files)
            st.session_state['uploaded_documents'].append(uploaded_file)
            
        if uploaded_files:
            st.session_state['file_uploaded'] = True
            st.session_state['page'] = 'document_selection'

def document_selection_page():
    if st.session_state['uploaded_documents']:
        doc_names = [doc.name for doc in st.session_state['uploaded_documents']]
        selected_doc = st.selectbox("Select a document to chat about", doc_names)
        if st.button('Confirm Selection'):
            st.session_state['selected_document'] = selected_doc
            st.session_state['page'] = 'chat_screen'
    else:
        st.write("No documents uploaded. Please upload documents first.")



def chat_screen_page():
    st.write("Chatbot interface goes here")
    chatclass = ChatClass(st.session_state['openaikey'], st.session_state['pineconekey'])


    if st.session_state['uploaded_documents']:
        doc_names = [doc.name for doc in st.session_state['uploaded_documents']]
        selected_doc = st.selectbox("Select a document to chat about", doc_names)
        
        if st.button('Confirm / Clear'):
            st.session_state['selected_document'] = selected_doc
            st.session_state['page'] = 'chat_screen'
            st.session_state.messages = []
            selected_doc = st.session_state['selected_document']
                
    else:
        st.write("No documents uploaded. Please upload documents first.")
        

    st.title("Simple chat")
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            # Simulate stream of response with milliseconds delay
            assistant_response = chatclass.getAnswer(prompt, selected_doc)
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Back Navigation Function
def go_back():
    if st.session_state['page'] == 'api_key_input':
        st.session_state['page'] = 'home'
    elif st.session_state['page'] == 'document_upload':
        st.session_state['page'] = 'api_key_input'
    # Add similar logic for other pages if needed

if 'uploaded_documents' not in st.session_state:
    st.session_state['uploaded_documents'] = []
if 'selected_document' not in st.session_state:
    st.session_state['selected_document'] = None


# Conditional Page Rendering
if st.session_state['page'] == 'home':
    home_page()
elif st.session_state['page'] == 'api_key_input' and not st.session_state['api_keys_validated']:
    api_key_input_page()
elif st.session_state['page'] == 'document_upload' and st.session_state['api_keys_validated'] and not st.session_state['file_uploaded']:
    document_upload_page()
elif st.session_state['page'] == 'document_selection' and st.session_state['file_uploaded']:
    document_selection_page()
elif st.session_state['page'] == 'chat_screen' and st.session_state['selected_document'] is not None:
    chat_screen_page()

