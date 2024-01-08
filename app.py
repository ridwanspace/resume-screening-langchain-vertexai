import streamlit as st
import os
import uuid
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.vectorstores import FAISS


# utils
from utils.create_docs import get_docs
from utils.embedding import create_embeddings_load_data
from utils.summarize import get_summary

# page config
st.set_page_config(
    page_title="Resume Screening Assistant",
    page_icon=":memo:",
)

# Sidebar contents
with st.sidebar:
   clear = st.button('Clear Cache Data') # clear cache (local vectore store)
   if clear:
       st.cache_data.clear()

st.title("HR - Resume Screening Assistance...💁 ")
st.subheader("Find the best candidates for the job using Vertex AI and LangChain")
job_description = st.text_area("Please paste the 'JOB DESCRIPTION' here...", key="1")
document_count = st.number_input("Number of 'Candidates' to be generated    ", min_value=1, max_value=10, key="2")

# upload a PDF file
pdf = st.file_uploader("Upload your PDF", type=['pdf'], accept_multiple_files=True)


# Get docs and check for submit
if pdf is not None:
    # session state
    st.session_state['unique_id']=uuid.uuid4().hex
    # create docs (list of Document objects)
    final_docs_list = get_docs(pdf, st.session_state['unique_id'])
    # submit button
    submit = st.button("Help me with the analysis")
    # start the process by clicking the submit button
    if submit:
        store_name = st.session_state['unique_id']
        # embedding
        embeddings = create_embeddings_load_data()
        # store to FAISS the list of docs as vector embedding
        db = FAISS.from_documents(final_docs_list, embeddings)
        db.save_local("faiss_index")
        print('Local FAISS index has been successfully saved.')
        
        ## load vector store
        VectorStore = FAISS.load_local("faiss_index", embeddings)
        
 
        # similarity search from vector store
        docs = VectorStore.similarity_search(query=job_description, k=int(document_count))
        # give the user some feedback
        st.success("The candidates are shown below from the top to bottom rank:")
        # iterate over the found docs
        for document in docs:
            page_content = document.page_content
            metadata = document.metadata
            
            # Access metadata attributes
            name = metadata.get('name', '')
            id = metadata.get('id', '')
            document_type = metadata.get('type', '')
            size = metadata.get('size', '')
            unique_id = metadata.get('unique_id', '')
            page_number = metadata.get('page_numbers', '')
            
            with st.expander('Show me the candidate👀'):
                st.write(f"Filename: {name}, Page: {page_number}") 
                # Gets the summary of the current item using 'get_summary' function that we have created which uses LLM & Langchain chain
                summary = get_summary(document)
                st.write(f"**Summary** : {summary}")
    
        st.write('Hope I was able to save your time❤️')
