from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import sqlite3
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API client
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API key not found! Please set the GOOGLE_API_KEY in your environment.")
    st.stop()

# Initialize the Gemini Pro model and chat session
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get a response from the Gemini model
def get_gemini_response(question):
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

# Add these functions after the imports and before the Streamlit app setup

def init_db():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat_messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  role TEXT,
                  content TEXT,
                  timestamp DATETIME)''')
    conn.commit()
    conn.close()

def save_message(role, content):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO chat_messages (role, content, timestamp) VALUES (?, ?, ?)",
              (role, content, datetime.now()))
    conn.commit()
    conn.close()

def get_chat_history():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("SELECT role, content FROM chat_messages ORDER BY timestamp DESC LIMIT 50")
    messages = c.fetchall()
    conn.close()
    return messages

# Initialize the Streamlit app
st.set_page_config(page_title="Kunal Pawar Chatbot", page_icon="🤖", layout="wide")

# Custom CSS to improve the UI
st.markdown("""
    <style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #e6f3ff;
        border: 1px solid #b3d9ff;
    }
    .chat-message.bot {
        background-color: #2b2b2b;
        border: 1px solid #444444;
        color: #ffffff;
    }
    .chat-message .message-content {
        margin-top: 0.5rem;
    }
    .chat-message.bot .message-content {
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Kunal Pawar Chatbot")
st.markdown("Welcome to Kunal Pawar! Ask me anything about education.")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input and submit button
input_text = st.text_input("Ask a question:", key="input")
submit = st.button("Send", key="submit")

if submit and input_text:
    response = get_gemini_response(input_text)
    
    # Save user message to database
    save_message("user", input_text)
    
    # Display response
    full_response = ""
    message_placeholder = st.empty()
    for chunk in response:
        full_response += chunk.text
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    
    # Save bot response to database
    save_message("bot", full_response)
elif submit:
    st.warning("Please enter a question.")

# Modify the chat history display to use the database
st.subheader("Chat History")
for role, text in get_chat_history():
    div_class = "chat-message user" if role == "user" else "chat-message bot"
    st.markdown(f"""
        <div class="{div_class}">
            <strong>{'You' if role == 'user' else 'Bot'}:</strong>
            <div class="message-content">{text}</div>
        </div>
    """, unsafe_allow_html=True)

# Modify the clear chat button to clear the database
if st.button("Clear Chat"):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("DELETE FROM chat_messages")
    conn.commit()
    conn.close()
    st.experimental_rerun()
