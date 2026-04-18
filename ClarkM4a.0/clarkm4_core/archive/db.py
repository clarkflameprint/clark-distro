import sqlite3
from datetime import datetime

DB_PATH = "clark_conversations.db"

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
