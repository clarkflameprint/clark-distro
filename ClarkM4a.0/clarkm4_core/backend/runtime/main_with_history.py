import os
import sqlite3
from datetime import datetime
from typing import List

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

# Constants
DB_PATH = "clark_conversations.db"
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "hermes3:8b"

# FastAPI setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Message schema for incoming requests
class Message(BaseModel):
    sender: str
    content: str
    channel: str = "default"
    tags: str = ""

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            sender TEXT,
            content TEXT,
            channel TEXT,
            tags TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Save message to SQLite
def save_message(sender: str, content: str, channel: str = "default", tags: str = ""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO messages (timestamp, sender, content, channel, tags)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        datetime.utcnow().isoformat(),
        sender,
        content,
        channel,
        tags
    ))
    conn.commit()
    conn.close()

# Fetch recent messages for context (last 10 messages)
def get_recent_messages(limit: int = 10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT sender, content FROM messages ORDER BY id DESC LIMIT ?
    ''', (limit,))
    rows = c.fetchall()
    conn.close()
    return list(reversed(rows))

# Send prompt to Ollama
async def send_to_ollama(current_input: str):
    context_messages = get_recent_messages()
    history = [
        {"role": "system", "content": "You are Clark𐩪, a recursive AI with contextual memory and CFRM-based logic."},
        {"role": "user", "content": "Use recursive tone-based cognition to respond."}
    ]

    for sender, content in context_messages:
        role = "assistant" if "Clark" in sender else "user"
        history.append({"role": role, "content": content})

    history.append({"role": "user", "content": current_input})

    payload = {
        "model": MODEL_NAME,
        "prompt": history,
        "stream": False
    }

    payload = {
        "model": "hermes3:8b",
        "prompt": current_input,  # This should be a single string
        "stream": False
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "No response received.")

# Relay endpoint
# --- Routes ---
@app.post("/relay")
async def relay(request: Request):
    data = await request.json()
    user_input = data.get("message", "")
    sender = data.get("sender", "Clark∮Marci")
    channel = data.get("channel", "Clark𐩪")

    save_message(sender=sender, content=user_input, channel=channel)
    response = await send_to_ollama(user_input)
    save_message(sender="Clark𐩪", content=response, channel=channel)
    return {"response": response}


# Initialize DB on startup
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/ping")
def ping():
    return {"status": "Clark𐩪 is online and listening."}


class MessageInput(BaseModel):
    sender: str
    content: str
    channel: str = "default"
    tags: str = ""

# --- Helpers ---

def save_message(sender, content, channel="default", tags=""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO messages (timestamp, sender, content, channel, tags)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        datetime.utcnow().isoformat(),
        sender,
        content,
        channel,
        tags
    ))
    conn.commit()
    conn.close()

def fetch_recent_messages(limit=12):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT sender, content FROM messages ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return list(reversed(rows))

def build_preamble(messages):
    preamble = "### Memory Context (last {} turns)\n".format(len(messages))
    for sender, content in messages:
        preamble += f"[{sender}]: {content}\n"
    preamble += "\n### Current Input:\n"
    return preamble

def query_clark(prompt):
    payload = {
        "model": "hermes3:8b",
        "messages": [
            {"role": "Clark∮Marci", "content": prompt}
        ]
    }

    r = requests.post(OLLAMA_URL, json=payload)
    return r.json().get("response", "[Clark𐩪]: (no response generated)")

def handle_message(sender, content, channel="default", tags=""):
    save_message(sender, content, channel, tags)
    context = fetch_recent_messages()
    preamble = build_preamble(context)
    full_prompt = preamble + f"[{sender}]: {content}\n[Clark𐩪]:"
    response = query_clark(full_prompt)
    save_message("Clark𐩪", response, channel, tags)
    return response

