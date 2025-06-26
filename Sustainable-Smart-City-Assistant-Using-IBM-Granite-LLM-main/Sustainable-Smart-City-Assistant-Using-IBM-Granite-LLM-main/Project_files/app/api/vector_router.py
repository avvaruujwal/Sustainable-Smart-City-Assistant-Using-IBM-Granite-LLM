from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_embedder import embed_and_store
import uuid

router = APIRouter(
    prefix="/vectors",
    tags=["Vector Search"]
)

@router.post("/upload-doc")
async def upload_document(file: UploadFile = File(...)):
    """
    Accepts a text document upload, embeds its content, and stores it in Pinecone.
    """
    if not file.content_type == "text/plain":
        raise HTTPException(status_code=400, detail="Only .txt files are supported.")

    try:
        contents = await file.read()
        text = contents.decode("utf-8")
        
        # Use a unique ID for the document chunk
        doc_id = str(uuid.uuid4())
        
        # In a real app, you might chunk the text into smaller pieces
        embed_and_store(doc_id=doc_id, text=text)
        
        return {
            "filename": file.filename,
            "doc_id": doc_id,
            "status": "embedding_successful"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process and embed file: {e}") 