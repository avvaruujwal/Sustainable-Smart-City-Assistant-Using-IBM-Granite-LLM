import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000" # This should be in a config file ideally

def render_chat_assistant():
    """
    Renders an interactive chat interface that communicates with the backend chat API.
    General-purpose AI assistant for any type of questions.
    """
    st.header("Chat with your Sustainable AI Assistant")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I’m your Sustainable City AI Assistant. 🌱🏙️ I'm here to support your journey toward building smarter, greener, and more resilient cities. Whether you need insights on energy consumption, water usage, waste management, or air quality, I’m ready to help you make data-driven decisions for a sustainable future."}
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            # Set font color to white for better visibility on dark backgrounds
            st.markdown(f'<div style="color: white;">{message["content"]}</div>', unsafe_allow_html=True)

    # Accept user input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(f'<div style="color: white;">{prompt}</div>', unsafe_allow_html=True)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            payload = {"prompt": prompt}
            try:
                # Call the backend API
                response = requests.post(f"{API_URL}/chat/ask", json=payload)
                response.raise_for_status()
                api_response = response.json().get("response", "Sorry, I couldn't get a response.")
                
                # For a streaming effect, you would iterate over the response here.
                # For now, we just display the full response.
                full_response = api_response

            except requests.exceptions.RequestException as e:
                full_response = f"Error: Unable to reach the chat service. Please ensure the backend is running."
            
            message_placeholder.markdown(f'<div style="color: white;">{full_response}</div>', unsafe_allow_html=True)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
 