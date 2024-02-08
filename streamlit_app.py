# importing the necessary libraries
import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

# configure Google API key
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))


# creating a function to load gemini pro vision model and get response
def get_gemini_response(input_message, image, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input_message, image[0], prompt])
    return response.text


# Function to convert uploaded image/PDF into bytes
def input_data_setup(uploaded_file):
    if uploaded_file is not None:
        # convert image to bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type, 
                "data": bytes_data
            }]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded!")
    

# Initializing streamlit app
st.set_page_config(page_title = "Invoice Extractor using Google Gemini Pro")

st.header("A.I Enabled Invoice Extractor", divider = True)

input_query = st.text_input("Input Prompt: ", key = "input")
uploaded_file = st.file_uploader("Browse an image....", type = ["jpg", "jpeg", "png"])

image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption = "Image uploaded successfuly.", use_column_width = True)

submit = st.button("Tell me about invoice")

input_prompt = """
You are an expert in understanding invoices. You will receive input images as invoices and you will have to answer questions based on the input image.              
"""

response = None

# Handle query submission
if submit:
    if not input_query:
        st.warning("Please provide a query.")
    else:
        if image is None:
            st.warning("Please upload an image.")
        else:
            try:
                image_data = input_data_setup(uploaded_file)
                response = get_gemini_response(input_prompt, image_data, input_query)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Display result
st.subheader(f"Result for the given query: {input_query}", divider = "rainbow")
if response is not None:
    st.write(response)