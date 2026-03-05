import streamlit as st
import requests
import os
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="QR Code Generator",
    page_icon="qr_code",
    layout="centered"
)

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/generate")

# Custom CSS for premium look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4F46E5;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        border-color: #4338CA;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🖼️ QR Code Generator")
st.markdown("Generate custom QR codes for your URLs, text, or location links instantly.")

# Sidebar for configuration
st.sidebar.header("Configuration")
box_size = st.sidebar.slider("Box Size", min_value=1, max_value=50, value=10)
border = st.sidebar.slider("Border Thickness", min_value=0, max_value=10, value=4)

# Main input area
data = st.text_area("Enter Text or URL", placeholder="e.g., https://www.google.com")

if st.button("Generate QR Code"):
    if not data:
        st.error("Please enter some data to generate a QR code.")
    else:
        with st.spinner("Generating..."):
            try:
                # Use the configured backend URL
                payload = {
                    "data": data,
                    "box_size": box_size,
                    "border": border
                }
                
                response = requests.post(BACKEND_URL, json=payload)
                
                if response.status_code == 200:
                    # Display the image
                    image_bytes = BytesIO(response.content)
                    st.image(image_bytes, caption="Generated QR Code", use_container_width=True)
                    
                    # Download button
                    st.download_button(
                        label="Download QR Code",
                        data=response.content,
                        file_name="qrcode.png",
                        mime="image/png"
                    )
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Could not connect to the backend server: {str(e)}")
                st.info("Make sure the FastAPI server is running with 'python main.py'")

st.markdown("---")
st.caption("Powered by FastAPI & Streamlit")
