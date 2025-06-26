import pandas as pd
from io import StringIO

def check_anomalies(file_content: str, std_dev_threshold: float = 2.0) -> dict:
    """
    Reads CSV data from a string and flags anomalies based on a standard 
    deviation threshold. Adds a description of the anomaly type.
    
    Assumes the CSV has at least a 'value' column.
    """
    df = pd.read_csv(StringIO(file_content))
    
    if 'value' not in df.columns:
        raise ValueError("Input CSV data must have a 'value' column for anomaly detection.")
        
    mean = df['value'].mean()
    std_dev = df['value'].std()
    
    # Define anomaly thresholds
    anomaly_threshold_upper = mean + (std_dev_threshold * std_dev)
    anomaly_threshold_lower = mean - (std_dev_threshold * std_dev)
    
    # Flag anomalies
    df['is_anomaly'] = (df['value'] > anomaly_threshold_upper) | (df['value'] < anomaly_threshold_lower)
    
    # Add anomaly type description
    def anomaly_type(row):
        if not row['is_anomaly']:
            return ''
        if row['value'] > anomaly_threshold_upper:
            return 'High anomaly (value much higher than expected)'
        elif row['value'] < anomaly_threshold_lower:
            return 'Low anomaly (value much lower than expected)'
        else:
            return 'Anomaly'
    df['anomaly_type'] = df.apply(anomaly_type, axis=1)
    
    anomalies = df[df['is_anomaly']]
    
    # Convert date to string for JSON serialization if it exists
    if 'date' in df.columns:
        df['date'] = df['date'].astype(str)

    return {
        "processed_data": df.to_dict(orient='records'),
        "anomalies_found": anomalies.to_dict('records') if len(anomalies) > 0 else [],
        "statistics": {
            "mean": mean,
            "std_dev": std_dev,
            "threshold_upper": anomaly_threshold_upper,
            "threshold_lower": anomaly_threshold_lower
        }
    } 