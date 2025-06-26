from fastapi import APIRouter
from pydantic import BaseModel
from app.services.granite_llm import generate_city_report

router = APIRouter(
    prefix="/report",
    tags=["Sustainability Report"]
)

class KpiData(BaseModel):
    # This model should be updated to reflect the actual KPI data structure
    data: dict

@router.post("/generate")
async def generate_report(kpi_data: KpiData):
    """
    Generates a city sustainability report based on provided KPI data.
    """
    report = generate_city_report(kpi_data.data)
    return {"report": report} 