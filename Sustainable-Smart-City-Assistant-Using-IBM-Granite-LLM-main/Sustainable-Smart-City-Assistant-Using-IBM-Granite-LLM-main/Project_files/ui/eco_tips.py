import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000" # This should be in a config file ideally

def render_eco_tips():
    """
    Renders an interface to get eco-friendly tips from the backend API.
    """
    st.header("🌿 Get Personalized Eco-Friendly Tips")
    
    # Remove the popular topics section
    # st.markdown("""
    # **Popular topics to try:**
    # - energy, water, waste, recycling, transport
    # - smart city, sustainable city, urban
    # - paper, plastic, food, garden, home
    # - office, school, community, business
    # """)
    
    topic = st.text_input("Enter a topic:", "")

    if st.button("Get Eco Tip"):
        if topic:
            with st.spinner("Generating eco-friendly tip..."):
                try:
                    params = {"topic": topic}
                    response = requests.get(f"{API_URL}/eco-tips/", params=params)
                    response.raise_for_status()
                    data = response.json()
                    tip = data.get("tip", "No tip found for this topic.")
                    
                    # Check if tip is meaningful
                    if tip and tip.strip():
                        st.success(f"💡 **Eco Tip for '{topic.capitalize()}'**:")
                        st.info(tip)
                    else:
                        st.warning("Couldn't generate a specific tip for that topic. Try a different keyword!")
                        st.info("💡 **General Eco Tip**: Reduce your carbon footprint by walking or cycling for short trips instead of driving.")
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to get tip. Could not connect to the API.")
                    st.info("💡 **Offline Eco Tip**: Turn off lights when leaving a room to save energy and reduce your electricity bill.")
        else:
            st.warning("Please enter a topic to get a tip.")
    
    # Remove quick tips section below
    # st.markdown("---")
    # st.subheader("🚀 Quick Tips")
    # 
    # col1, col2, col3 = st.columns(3)
    # 
    # with col1:
    #     if st.button("💡 Energy Tip"):
    #         st.info("Switch to LED light bulbs which use 75% less energy and last 25 times longer than incandescent bulbs.")
    # 
    # with col2:
    #     if st.button("💧 Water Tip"):
    #         st.info("Install low-flow showerheads and faucets to reduce water consumption by up to 50%.")
    # 
    # with col3:
    #     if st.button("♻️ Recycling Tip"):
    #         st.info("Set up separate bins for paper, plastic, glass, and metal to make recycling easier and more effective.") 