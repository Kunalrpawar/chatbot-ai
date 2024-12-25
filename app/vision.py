import streamlit as st
import google.generativeai as genai
from PIL import Image
from config.config import Config

# Configure the Gemini API client
genai.configure(api_key=Config.GOOGLE_API_KEY)

# Initialize the Gemini Pro Vision model
model = genai.GenerativeModel('gemini-pro-vision')

def analyze_image(image, prompt):
    try:
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        st.error(f"Error analyzing image: {str(e)}")
        return None

def vision_app():
    st.title("🖼️ Movie Poster Scanner")
    st.markdown("Upload a movie poster to get information about the film!")

    uploaded_file = st.file_uploader("Choose a movie poster...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Movie Poster", use_column_width=True)

        if st.button("Analyze Poster"):
            with st.spinner("Analyzing..."):
                prompt = "Analyze this movie poster. Identify the movie title, main actors, genre, and provide a brief synopsis if possible."
                analysis_result = analyze_image(image, prompt)
                if analysis_result:
                    st.markdown("### Movie Information:")
                    st.write(analysis_result)
                else:
                    st.warning("Failed to analyze the poster. Please try again.")

if __name__ == "__main__":
    vision_app()
