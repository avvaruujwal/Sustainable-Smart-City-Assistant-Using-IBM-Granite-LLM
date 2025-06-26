from fastapi import APIRouter

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

# Endpoints for aggregated dashboard data will be added here.
# For example: GET /kpi-summary 