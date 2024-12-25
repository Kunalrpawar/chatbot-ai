import streamlit as st
import google.generativeai as genai
from config.config import Config
from app.database import save_message, get_chat_history, clear_chat_history, get_message_count

# Configure the Gemini API client
if Config.GOOGLE_API_KEY:
    genai.configure(api_key=Config.GOOGLE_API_KEY)
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

def qachat_app():
    st.title("🤖 Kunal Pawar Chatbot")
    st.markdown("Welcome to Kunal Pawar! Ask me anything about education.")

    # Display database statistics
    message_count = get_message_count()
    st.sidebar.markdown(f"**Total messages in database:** {message_count}")

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

        # Update message count
        message_count = get_message_count()
        st.sidebar.markdown(f"**Total messages in database:** {message_count}")

    elif submit:
        st.warning("Please enter a question.")

    # Display chat history
    st.subheader("Chat History")
    for role, text in get_chat_history():
        div_class = "chat-message user" if role == "user" else "chat-message bot"
        st.markdown(f"""
            <div class="{div_class}">
                <strong>{'You' if role == 'user' else 'Bot'}:</strong>
                <div class="message-content">{text}</div>
            </div>
        """, unsafe_allow_html=True)

    # Clear chat button
    if st.button("Clear Chat"):
        clear_chat_history()
        st.experimental_rerun()

# Custom CSS (you can keep this part in the qachat_app function)
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
