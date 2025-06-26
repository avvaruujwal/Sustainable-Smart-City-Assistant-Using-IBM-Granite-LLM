import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000" # This should be in a config file ideally

def render_feedback_form():
    """
    Renders a form to collect and submit user feedback via API.
    """
    st.header("We'd Love Your Feedback!")
    with st.form("feedback_form", clear_on_submit=True):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message", height=150)
        
        submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            if not all([name, email, message]):
                st.warning("Please fill out all fields before submitting.")
            else:
                payload = {"name": name, "email": email, "message": message}
                try:
                    response = requests.post(f"{API_URL}/feedback/submit", json=payload)
                    response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
                    st.success("Thank you for your feedback! It has been submitted successfully.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to submit feedback. Could not connect to the API. Please ensure the backend is running.") 