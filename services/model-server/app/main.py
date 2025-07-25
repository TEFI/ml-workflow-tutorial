from fastapi import FastAPI
from app.routes import router

# Create FastAPI application
app = FastAPI(
    title="ML Inference API",
    description="A lightweight API to serve machine learning model predictions.",
    version="0.1.0"
)

# Register API routes
app.include_router(router)