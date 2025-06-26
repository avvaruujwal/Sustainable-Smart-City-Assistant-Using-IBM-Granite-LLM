from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.kpi_file_forecaster import forecast_kpi
from app.services.anomaly_file_checker import check_anomalies

router = APIRouter(
    prefix="/kpi",
    tags=["KPI Data"]
)

@router.post("/upload")
async def upload_kpi_file(file: UploadFile = File(...)):
    """
    Accepts a CSV file with KPI data for forecasting and anomaly detection.
    (Placeholder: a real implementation would process the CSV data)
    """
    # Logic for parsing the CSV and running ML models will be added here.
    return {"filename": file.filename, "content_type": file.content_type, "status": "placeholder_kpi_upload_successful"}

@router.post("/forecast")
async def get_kpi_forecast(file: UploadFile = File(...)):
    """
    Accepts a CSV file with historical KPI data and returns a 30-day forecast.
    """
    if not file.content_type == "text/csv":
        raise HTTPException(status_code=400, detail="Only .csv files are supported.")
    
    try:
        contents = await file.read()
        file_content_str = contents.decode("utf-8")
        forecast = forecast_kpi(file_content_str)
        return forecast
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate forecast: {e}")

@router.post("/anomaly-check")
async def get_kpi_anomalies(file: UploadFile = File(...)):
    """
    Accepts a CSV file with KPI data and returns any detected anomalies.
    """
    if not file.content_type == "text/csv":
        raise HTTPException(status_code=400, detail="Only .csv files are supported.")
    
    try:
        contents = await file.read()
        file_content_str = contents.decode("utf-8")
        anomalies = check_anomalies(file_content_str)
        return anomalies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check for anomalies: {e}") 