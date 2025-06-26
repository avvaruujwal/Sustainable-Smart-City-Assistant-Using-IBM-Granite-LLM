import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from io import StringIO

def forecast_kpi(file_content: str) -> dict:
    """
    Reads CSV data from a string, trains a linear regression model, 
    and returns a forecast for the next 30 periods.
    
    Assumes the CSV has two columns: 'date' and 'value'.
    """
    df = pd.read_csv(StringIO(file_content))
    
    # Basic data validation
    if 'date' not in df.columns or 'value' not in df.columns:
        raise ValueError("Input CSV data must have 'date' and 'value' columns.")
        
    df['date'] = pd.to_datetime(df['date'])
    # Convert date to a numerical format for regression
    df['time'] = (df['date'] - df['date'].min()).dt.days
    
    X = df[['time']]
    y = df['value']
    
    if len(df) < 2:
        raise ValueError("Need at least two data points to perform a forecast.")

    model = LinearRegression()
    model.fit(X, y)
    
    # Create future time points to predict
    last_time = X['time'].max()
    future_time_points = np.array(range(last_time + 1, last_time + 31)).reshape(-1, 1)
    
    # Predict future values
    forecast_values = model.predict(future_time_points)
    
    # Create future dates for the forecast
    last_date = df['date'].max()
    future_dates = pd.to_datetime([last_date + pd.DateOffset(days=i) for i in range(1, 31)])
    
    # Combine dates and forecasted values
    forecast_df = pd.DataFrame({'date': future_dates, 'forecasted_value': forecast_values})
    
    # Convert dates to string for JSON serialization
    forecast_df['date'] = forecast_df['date'].dt.strftime('%Y-%m-%d')

    return {
        "original_data": df.to_dict(orient='records'),
        "forecast_data": forecast_df.to_dict(orient='records')
    } 