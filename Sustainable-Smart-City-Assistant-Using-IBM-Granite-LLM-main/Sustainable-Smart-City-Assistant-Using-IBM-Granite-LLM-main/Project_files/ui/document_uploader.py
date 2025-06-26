import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000" # This should be in a config file ideally

def render_document_uploader():
    """
    Renders an interface for uploading documents to be embedded.
    """
    st.header("Upload a Policy Document")
    st.info("Upload a plain text (.txt) file to be embedded and indexed for semantic search.")
    
    uploaded_file = st.file_uploader("Choose a file", type=['txt'])

    if uploaded_file is not None:
        if st.button("Upload and Embed Document"):
            with st.spinner("Uploading and processing file..."):
                files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'text/plain')}
                try:
                    response = requests.post(f"{API_URL}/vectors/upload-doc", files=files)
                    response.raise_for_status()
                    data = response.json()
                    st.success(f"File '{data['filename']}' uploaded successfully! (Doc ID: {data['doc_id']})")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred during upload: {e}") 