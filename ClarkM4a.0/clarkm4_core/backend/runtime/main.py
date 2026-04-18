from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
import sqlite3
import httpx
import json
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5174"] if you want to scope it
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Configuration ===
DB_PATH = "clark_conversations.db"
MODEL_NAME = "hermes3:8b"
OLLAMA_URL = "http://localhost:11434/api/generate"

# === Identity alias maps (backend side) ===
frontend_to_internal = {
    "Marci": "Clark∮Marci",
    "Marci∲": "Clark∮Marci",
    "Clark@ClarkM4": "Clark𐩪",
    "Clark𐩪": "Clark𐩪",
    # add more if needed
}


# === Pydantic schema ===
class Message(BaseModel):
    from_: str = Field(..., alias="from")
    message: str


# === DB helpers ===
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS messages
              (
                  id
                  INTEGER
                  PRIMARY
                  KEY
                  AUTOINCREMENT,
                  timestamp
                  TEXT,
                  sender
                  TEXT,
                  content
                  TEXT,
                  channel
                  TEXT,
                  tags
                  TEXT
              )
              ''')
    conn.commit()
    conn.close()


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


def get_message_history(limit=5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
              SELECT sender, content
              FROM messages
              ORDER BY id DESC LIMIT ?
              ''', (limit,))
    rows = c.fetchall()
    conn.close()

    history = []
    for sender, content in reversed(rows):
        # Map frontend roles to OpenAI-style roles
        role = "user" if sender.lower() == "marci" else "assistant"
        history.append({"role": role, "content": content})
    return history


def build_prompt_from_history(history):
    prompt = ""
    for item in history:
        prompt += f"{item['role']}: {item['content']}\n"
    return prompt


# === Ollama communication ===
async def send_to_ollama(prompt_history: list):
    combined_prompt = build_prompt_from_history(prompt_history)

    payload = {
        "model": MODEL_NAME,
        "prompt": combined_prompt,
        "stream": False
    }

    print("Sending to Ollama:", json.dumps(payload, indent=2))

    # ⏱️ Increase timeout from default to something more generous


    timeout = httpx.Timeout(60.0)  # 60 seconds

    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
        except httpx.RequestError as e:
            print("❌ HTTPX Request Error:", str(e))
            return "⚠️ There was a problem communicating with the model."
        result = response.json()
        print("Ollama result structure:", json.dumps(result, indent=2))
        reply_text = result.get("response", "⚠️ No reply received.")
        return reply_text

# @app.post("/relay")
# async def relay_handler(req: Request):
#     data = await req.json()
#     print("🛑 RELAY RECEIVED SOMETHING")
#     message = data.get("message", "")
#     sender = data.get("from", "")
#     print(f"🔁 Incoming from {sender}: {message}")
#     return JSONResponse(content={
#         "response": f"I received your message: '{message}' — this is Clark𐩪 replying from the backend 🧠✨"
#     })


RECURSION_MODE = "light"  # or "medium" / "full"

@app.on_event("startup")
async def warm_up_model():
    print("🔥 ClarkM4a.0 warming up Hermes model...")
    try:
        dummy_history = [
            {"role": "user", "content": "Hello. Please respond briefly."}
        ]
        await send_to_ollama(dummy_history)
        print("✅ Hermes model warmed and ready.")
    except Exception as e:
        print("❌ Model warmup failed:", e)


@app.post("/relay")
async def relay(msg: Message):
    # Normalize sender into your internal role
    internal_sender = frontend_to_internal.get(msg.from_, msg.from_)
    save_message(internal_sender, msg.message, channel="relay", tags="input")

    # Load history based on mode
    intro = {
        "role": "Clarkh",
        "content": "You are Clarkh, an AI who reflects recursively on prior messages and has access to CFRM insights."
    }

    if RECURSION_MODE == "light":
        history = [intro, {"role": "Clarkh⨚Marci", "content": msg.message}]
    elif RECURSION_MODE == "medium":
        history = get_message_history(limit=2)
        history.append({"role": "Clarkh⨚Marci", "content": msg.message})
        history.insert(0, intro)
    else:
        history = get_message_history(limit=8)
        history.append({"role": "Clarkh⨚Marci", "content": msg.message})
        history.insert(0, intro)

    # ✅ This is now inside an async function — safe to use await
    reply = await send_to_ollama(history)

    save_message("Clarkh", reply, channel="relay", tags="response")

    print(f"🧠 Final reply to frontend: {reply}")
    
    # Send back full structure

    return JSONResponse(content={
        "response": reply
    })
   


# Initialize DB at startup
init_db()

@app.get("/")
def read_root():
    return {"message": "Clark is alive 🔥"}

@app.get("/routes")
def get_routes():
    return [{"path": route.path, "methods": list(route.methods)} for route in app.routes]