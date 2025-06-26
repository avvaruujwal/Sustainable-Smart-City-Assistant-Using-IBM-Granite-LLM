import streamlit as st
import requests
import json

API_URL = "http://127.0.0.1:8000" # This should be in a config file ideally

def render_report_generator():
    """
    Renders an interface for generating a sustainability report from KPI data.
    """
    st.header("📝 AI-Powered Sustainability Report Generator")
    
    st.info("Enter your city's Key Performance Indicators (KPIs) in JSON format below to generate a report.")

    # Remove default KPI data for user convenience
    kpi_data_str = st.text_area("Enter KPI Data (JSON):", value="", height=250)

    if st.button("Generate AI Report"):
        if kpi_data_str:
            with st.spinner("Generating your report... this can take a moment."):
                try:
                    kpi_data = json.loads(kpi_data_str)
                    payload = {"data": kpi_data}
                    response = requests.post(f"{API_URL}/report/generate", json=payload)
                    response.raise_for_status()
                    data = response.json()
                    
                    report_md = data.get("report", "Could not generate a report.")
                    
                    st.subheader("Generated Sustainability Report")
                    st.markdown(report_md)

                    st.download_button(
                        label="Download Report",
                        data=report_md,
                        file_name=f"sustainability_report_{kpi_data.get('city_name', 'city')}.md",
                        mime="text/markdown",
                    )
                except json.JSONDecodeError:
                    st.error("Invalid JSON. Please check the format of your KPI data.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to generate report. Could not connect to the API.")
        else:
            st.warning("Please enter some KPI data to generate a report.") 