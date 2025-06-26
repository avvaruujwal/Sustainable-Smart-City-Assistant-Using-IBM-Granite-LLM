import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000" # This should be in a config file ideally

def render_anomaly_checker():
    """
    Renders an interface for uploading KPI data and checking for anomalies.
    """
    st.header("🕵️ Anomaly Checker")
    st.info("Upload a CSV file with a 'value' column to detect unusual data points.")

    uploaded_file = st.file_uploader("Upload your historical data", type=['csv'], key="anomaly_uploader")

    if uploaded_file is not None:
        if st.button("Check for Anomalies"):
            with st.spinner("Analyzing data for anomalies..."):
                files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'text/csv')}
                try:
                    response = requests.post(f"{API_URL}/kpi/anomaly-check", files=files)
                    response.raise_for_status()
                    data = response.json()
                    
                    processed_df = pd.DataFrame(data['processed_data'])
                    anomalies_df = pd.DataFrame(data['anomalies_found'])
                    stats = data['statistics']
                    
                    st.subheader("Analysis Results")

                    if 'date' in processed_df.columns:
                        processed_df['date'] = pd.to_datetime(processed_df['date'])
                        chart_df = processed_df.set_index('date')
                    else:
                        chart_df = processed_df
                    
                    st.line_chart(chart_df['value'])
                    
                    if not anomalies_df.empty:
                        st.warning(f"Found {len(anomalies_df)} potential anomalies.")
                        st.dataframe(anomalies_df)
                    else:
                        st.success("No significant anomalies were detected.")

                    with st.expander("See Statistical Details"):
                        st.write(f"Mean: {stats['mean']:.2f}")
                        st.write(f"Standard Deviation: {stats['std_dev']:.2f}")
                        st.write(f"Upper Anomaly Threshold: {stats['threshold_upper']:.2f}")
                        st.write(f"Lower Anomaly Threshold: {stats['threshold_lower']:.2f}")

                except requests.exceptions.RequestException as e:
                    st.error(f"Analysis failed. Could not connect to the API.")
                except Exception as e:
                    st.error(f"An error occurred: {e}") 