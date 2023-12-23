import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Streamlit! 👋")

st.sidebar.success("Select a demo above.")

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

st.link_button('Get Started','https://0.0.0.0:8502/Verify_API_Key')