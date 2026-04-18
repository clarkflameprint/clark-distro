from datetime import datetime
import sqlite3
import requests

DB_PATH = "clark_conversations.db"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "hermes3:8b"

def fetch_recent_messages(limit=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT sender, content FROM messages ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    # newest first → oldest first
    return list(reversed(rows))

def build_preamble(messages):
    preamble = "### Memory Context (last {} turns)\n".format(len(messages))
    for sender, content in messages:
        preamble += f"[{sender}]: {content}\n"
    preamble += "\n### Current Input:\n"
    return preamble

def query_clark(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    r = requests.post(OLLAMA_URL, json=payload)
    return r.json()["response"]

def handle_message(sender, content):
    # 1. Save user message
    save_message(sender, content)
    # 2. Build preamble
    context = fetch_recent_messages(limit=12)
    preamble = build_preamble(context)
    # 3. Query model
    full_prompt = preamble + f"[{sender}]: {content}\n[Clark𐩪]:"
    response = query_clark(full_prompt)
    # 4. Save Clark𐩪 response
    save_message("Clark𐩪", response)
    return response

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

