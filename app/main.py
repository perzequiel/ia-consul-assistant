# app/main.py
from fastapi import FastAPI, Request
import requests
from pydantic import BaseModel

app = FastAPI()

class MessageInput(BaseModel):
    message: str

@app.post("/webhook")
async def chat(input: MessageInput):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "phi4", "prompt": input.message, "stream": False}
    ).json()
    reply = response.get("response", "No response from model.")
    return {"reply": reply}