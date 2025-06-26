import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000" # This should be in a config file ideally

def render_kpi_forecasting():
    """
    Renders an interface for uploading KPI data and viewing a forecast.
    """
    st.header("📈 KPI Forecasting Tool")
    st.info("Upload a CSV file with 'date' and 'value' columns to generate a 30-day forecast.")

    uploaded_file = st.file_uploader("Upload your historical KPI data", type=['csv'])

    if uploaded_file is not None:
        if st.button("Generate Forecast"):
            with st.spinner("Generating forecast..."):
                files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'text/csv')}
                try:
                    response = requests.post(f"{API_URL}/kpi/forecast", files=files)
                    response.raise_for_status()
                    data = response.json()
                    
                    original_df = pd.DataFrame(data['original_data'])
                    forecast_df = pd.DataFrame(data['forecast_data'])
                    
                    # Convert date columns to datetime objects for plotting
                    original_df['date'] = pd.to_datetime(original_df['date'])
                    forecast_df['date'] = pd.to_datetime(forecast_df['date'])
                    
                    st.subheader("Forecast Results")
                    
                    # Prepare data for charting
                    historical_data = original_df.set_index('date')[['value']]
                    historical_data.columns = ['Historical']
                    
                    forecast_data = forecast_df.set_index('date')[['forecasted_value']]
                    forecast_data.columns = ['Forecast']
                    
                    chart_data = pd.concat([historical_data, forecast_data], axis=1)
                    
                    st.line_chart(chart_data)

                    st.write("Forecasted Data:")
                    st.dataframe(forecast_df)

                except requests.exceptions.RequestException as e:
                    st.error(f"Forecast generation failed. Could not connect to the API.")
                except Exception as e:
                    st.error(f"An error occurred: {e}") 