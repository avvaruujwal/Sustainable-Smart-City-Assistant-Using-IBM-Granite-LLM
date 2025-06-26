from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.granite_llm import ask_city_question, get_sustainability_tips

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

class ChatRequest(BaseModel):
    prompt: str

class TipsRequest(BaseModel):
    category: str

@router.post("/ask")
async def ask(request: ChatRequest):
    """
    Accepts a user's prompt and returns a response from the AI chat assistant.
    Enhanced for comprehensive city-related questions.
    """
    response = ask_city_question(prompt=request.prompt)
    return {"response": response}

@router.post("/tips")
async def get_tips(request: TipsRequest):
    """
    Get sustainability tips for specific categories.
    """
    response = get_sustainability_tips(category=request.category)
    return {"response": response} 