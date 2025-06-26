from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"]
)

class Feedback(BaseModel):
    name: str
    email: str
    message: str

@router.post("/submit")
async def submit_feedback(feedback: Feedback):
    """
    Receives and processes user feedback.
    (Placeholder: in a real app, this would be saved to a database)
    """
    print(f"Feedback received from {feedback.name} ({feedback.email}): {feedback.message}")
    return {"status": "success", "message": "Thank you for your feedback!"} 