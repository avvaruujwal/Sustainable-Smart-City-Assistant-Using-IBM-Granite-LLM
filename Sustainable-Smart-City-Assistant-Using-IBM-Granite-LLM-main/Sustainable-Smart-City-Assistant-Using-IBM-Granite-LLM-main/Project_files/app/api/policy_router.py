from fastapi import APIRouter
from pydantic import BaseModel
from app.services.granite_llm import generate_summary
from app.services.document_embedder import search_documents


router = APIRouter(
    prefix="/policy",
    tags=["Policy"]
)

class PolicyText(BaseModel):
    text: str

@router.post("/summarize")
async def summarize_policy(policy_text: PolicyText):
    """
    Accepts a block of text and returns an AI-generated summary.
    """
    summary = generate_summary(policy_text.text)
    return {"original_text": policy_text.text, "summary": summary}


@router.get("/search-docs")
async def search_policies(query: str, top_k: int = 5):
    """
    Searches for relevant policy documents based on a query and returns summaries for each result.
    """
    results = search_documents(query=query, top_k=top_k)
    # Add summary for each result using Granite LLM
    for result in results:
        doc_text = result.get("metadata", {}).get("text", "")
        print(f"[DEBUG] Document text to summarize (id={result.get('id')}):\n{doc_text}\n---")
        if doc_text:
            summary = generate_summary(doc_text)
            print(f"[DEBUG] Summary generated (id={result.get('id')}):\n{summary}\n---")
            if not summary or not summary.strip():
                summary = "[ERROR] Granite LLM returned an empty summary."
            result["summary"] = summary
        else:
            result["summary"] = "No text available to summarize."
    return {"query": query, "results": results}


# Endpoints for policy search will be added here.
# For example: GET /search-docs 