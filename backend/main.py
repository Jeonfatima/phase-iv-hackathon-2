from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Import models to register them with SQLModel metadata
from models.conversation import Conversation, Message
from models.task import Task
from database.engine import engine, validate_database_connection
from api.auth import router as auth_router
from api.task_router import router as task_router
from api.chat import router as chat_router
from core.config import Settings

app = FastAPI(title="Todo API", version="0.1.0")

# ✅ CORS (correct)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://todoappphase3-hdsttxkhd-fatima-salmans-projects.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ROUTERS (order matters)
app.include_router(auth_router)
app.include_router(task_router)
app.include_router(chat_router)

@app.on_event("startup")
async def startup_event():
    # Validate settings first
    Settings.validate()
    SQLModel.metadata.create_all(bind=engine)
    validate_database_connection()

@app.get("/")
def read_root():
    return {"status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
