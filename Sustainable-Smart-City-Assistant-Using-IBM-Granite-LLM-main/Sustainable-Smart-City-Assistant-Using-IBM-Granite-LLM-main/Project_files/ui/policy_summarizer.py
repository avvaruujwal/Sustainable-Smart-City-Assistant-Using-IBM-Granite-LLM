import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000" # This should be in a config file ideally

def render_policy_summarizer():
    """
    Renders an interface for summarizing text using the backend API.
    """
    st.header("📜 Policy Document Summarizer")
    
    st.info("Paste the text from a policy document below to get an AI-generated summary.")

    policy_text = st.text_area(
        "Enter Policy Text:", 
        height=250, 
        placeholder="Paste your policy text here..."
    )

    if st.button("Generate Summary"):
        if policy_text:
            with st.spinner("Generating summary... this may take a moment."):
                try:
                    payload = {"text": policy_text}
                    response = requests.post(f"{API_URL}/policy/summarize", json=payload)
                    response.raise_for_status()
                    data = response.json()
                    
                    st.subheader("Generated Summary")
                    st.success(data.get("summary", "Could not generate a summary."))

                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to generate summary. Could not connect to the API.")
        else:
            st.warning("Please paste some text into the text area to summarize.") 