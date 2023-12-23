# Chat with your Documents
Use this project to upload and chat with your PDFs. You can use this tool to ask questions about the documents with the help of Gen AI. 


## Overview of the Project 

How does this tool work you may ask? Well here is the general breakdown of the flow of the program. 

In general when you use tools like OpenAI's ChatGPT or Google's Bard, you can only ask it questions from the general knowledge base that it accumulated during training. What if you want to have a conversation about a PDF file that you may have locally? 
In this tool, you can leverage the language capability of OpenAI's ChatGPT to converse with your files. You can upload multiple files (Upto 200MB) and set to asking questions about the content of these files. 

This tool achieves this by using the following flow : 

![Blank board](https://github.com/Bhavinrathava/ContextAwareAgent/assets/20955858/ab67e35c-8d8e-4429-a322-bd8b554122fe)

1. Your chat history and Current question and fed to ChatGPT to generate 1 question based on context and is also converted to embeddings
2. Your uploaded documents are converted to chunks, embedded and stored in a Pinecone DB
3. The embedded question is used to do semantic search on the pool of chunks created for your document in step 2 and the K most relevant chunks from source material are selected
4. The relevant source chunks + Generated question is fed to ChatGPT for the final answer

   
## Requirements 
1. OpenAI API Key
2. PineCone API Key
   

## Libraries and Frameworks Used

1. Langchain - For Recursive text splitting
2. OpenAI - For calls to Models and Embeddings
3. Streamlit - for frontend

## How to run this locally 

To run this locally, 
1. Create a virtual environment and install the dependencies from requirements.txt
2. Create OpenAI and Pinecone Accounts if not created already and get the API keys for both these platforms
3. In the main working directory, use 

'''
streamlit run Home.py --server.port=8501 --server.address=0.0.0.0
'''
