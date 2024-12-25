import streamlit as st
import google.generativeai as genai
from config.config import Config
from app.database import save_message, get_chat_history, clear_chat_history

# Configure the Gemini API client
genai.configure(api_key=Config.GOOGLE_API_KEY)

# Initialize the Gemini Pro model
model = genai.GenerativeModel('gemini-pro')

def chat_app(message):
    try:
        response = model.generate_content(message)
        return response.text
    except Exception as e:
        print(f"Error in chat_app: {str(e)}")
        return "I'm sorry, I encountered an error while processing your request."

def get_gemini_response(question):
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

def chat_app():
    st.title("🎬 Movie Chat")
    st.markdown("Chat about movies, ask for recommendations, or discuss your favorite films!")

    input_text = st.text_input("Ask a question about movies:", key="movie_input")
    submit = st.button("Send", key="movie_submit")

    if submit and input_text:
        response = get_gemini_response(input_text)
        
        save_message("user", input_text)
        
        full_response = ""
        message_placeholder = st.empty()
        for chunk in response:
            full_response += chunk.text
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        
        save_message("bot", full_response)

    elif submit:
        st.warning("Please enter a question.")

    st.subheader("Chat History")
    for role, text in get_chat_history():
        div_class = "chat-message user" if role == "user" else "chat-message bot"
        st.markdown(f"""
            <div class="{div_class}">
                <strong>{'You' if role == 'user' else 'Bot'}:</strong>
                <div class="message-content">{text}</div>
            </div>
        """, unsafe_allow_html=True)

    if st.button("Clear Chat History"):
        clear_chat_history()
        st.experimental_rerun()
