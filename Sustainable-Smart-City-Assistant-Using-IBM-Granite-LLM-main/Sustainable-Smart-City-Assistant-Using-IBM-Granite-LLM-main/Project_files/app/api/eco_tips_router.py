from fastapi import APIRouter
from app.services.granite_llm import generate_eco_tip

router = APIRouter(
    prefix="/eco-tips",
    tags=["Eco Tips"]
)

@router.get("/")
async def get_eco_tips(topic: str):
    """
    Provides an eco-friendly tip on a specified topic.
    """
    tip = generate_eco_tip(topic)
    return {"topic": topic, "tip": tip} 