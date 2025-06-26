from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import (
    chat_router,
    policy_router,
    eco_tips_router,
    feedback_router,
    report_router,
    vector_router,
    kpi_upload_router,
    dashboard_router,
)
from app.services.document_embedder import create_pinecone_index_if_not_exists

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    print("Application startup...")
    create_pinecone_index_if_not_exists()
    yield
    # On shutdown
    print("Application shutdown...")

app = FastAPI(
    title="Smart City Dashboard API",
    description="API for the Smart City Dashboard, powered by IBM Watsonx and Pinecone.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(chat_router.router)
app.include_router(policy_router.router)
app.include_router(eco_tips_router.router)
app.include_router(feedback_router.router)
app.include_router(report_router.router)
app.include_router(vector_router.router)
app.include_router(kpi_upload_router.router)
app.include_router(dashboard_router.router)

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the Smart City Dashboard API"} 