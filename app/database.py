import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('netflix_clone.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat_messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  role TEXT,
                  content TEXT,
                  timestamp DATETIME)''')
    conn.commit()
    conn.close()

def save_message(role, content):
    conn = sqlite3.connect('netflix_clone.db')
    c = conn.cursor()
    c.execute("INSERT INTO chat_messages (role, content, timestamp) VALUES (?, ?, ?)",
              (role, content, datetime.now()))
    conn.commit()
    conn.close()

def get_chat_history():
    conn = sqlite3.connect('netflix_clone.db')
    c = conn.cursor()
    c.execute("SELECT role, content FROM chat_messages ORDER BY timestamp DESC LIMIT 50")
    messages = c.fetchall()
    conn.close()
    return messages

def clear_chat_history():
    conn = sqlite3.connect('netflix_clone.db')
    c = conn.cursor()
    c.execute("DELETE FROM chat_messages")
    conn.commit()
    conn.close()

def get_message_count():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM chat_messages")
    count = c.fetchone()[0]
    conn.close()
    return count
