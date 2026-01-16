#!/usr/bin/env python3
"""
Simple test server to debug the actual error
"""

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging
import traceback
import sys

# Set up logging to see errors
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Import after loading environment
from core.config import Settings
from database.engine import engine, validate_database_connection
from sqlmodel import SQLModel
from api.chat import router as chat_router

app = FastAPI(title="Todo API Debug", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the chat router
app.include_router(chat_router)

@app.on_event("startup")
async def startup_event():
    # Validate settings first
    Settings.validate()
    SQLModel.metadata.create_all(bind=engine)
    validate_database_connection()
    logger.info("Startup completed")

@app.get("/")
def read_root():
    return {"status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Add middleware to catch and log errors
@app.middleware("http")
async def log_errors(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Error processing request {request.method} {request.url}: {e}")
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")