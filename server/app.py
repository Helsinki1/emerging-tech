# FastAPI backend
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vectordb_new import query_vectorDB
import openai
import os

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://10.207.123.211:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],  # Explicitly include OPTIONS
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=86400,  # Cache preflight requests for 24 hours
)

class UserInput(BaseModel):
    user_text: str

@app.post("/submit")
async def submit_user_input(data: UserInput):
    try:
        query = data.user_text
        companies = query_vectorDB(query)
        return {
            "status": "success",
            "companies": companies
        }
    except Exception as e:
        print("Error:", str(e))  # For debugging
        return {"status": "error", "detail": str(e)}
    