import streamlit as st
import google.generativeai as genai
from PIL import Image
from config.config import Config

# Configure the Gemini API client
if Config.GOOGLE_API_KEY:
    genai.configure(api_key=Config.GOOGLE_API_KEY)
else:
    st.error("API key not found! Please set the GOOGLE_API_KEY in your environment.")
    st.stop()

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
    st.title("🖼️ Kunal Pawar Image Analyzer")
    st.markdown("Upload an image and ask questions about it!")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        prompt = st.text_input("Ask a question about the image:")

        if st.button("Analyze Image"):
            if prompt:
                with st.spinner("Analyzing..."):
                    analysis_result = analyze_image(image, prompt)
                    if analysis_result:
                        st.markdown("### Analysis Result:")
                        st.write(analysis_result)
                    else:
                        st.warning("Failed to analyze image. Please try again.")
            else:
                st.warning("Please enter a question about the image.")

if __name__ == "__main__":
    vision_app()
