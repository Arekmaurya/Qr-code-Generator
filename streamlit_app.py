import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

# Set page configuration
st.set_page_config(
    page_title="QR Code Generator",
    page_icon="🖼️",
    layout="centered"
)

# Custom CSS for premium look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #4F46E5;
        color: white;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

def generate_qr(data, box_size, border):
    """Generates a QR code image."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

st.title("🖼️ QR Code Generator")
st.markdown("Generate custom QR codes for your URLs, text, or location links instantly. Optimized for Streamlit Cloud.")

# Sidebar for configuration
st.sidebar.header("⚙️ Configuration")
box_size = st.sidebar.slider("Box Size", min_value=1, max_value=50, value=10, help="Size of each square in the QR code.")
border = st.sidebar.slider("Border Thickness", min_value=0, max_value=10, value=4, help="Thickness of the white border.")

# Main input area
data = st.text_area("🔗 Enter Text or URL", placeholder="e.g., https://www.google.com", help="The content you want to encode in the QR code.")

if st.button("Generate QR Code"):
    if not data:
        st.error("Please enter some data to generate a QR code.")
    else:
        with st.spinner("✨ Creating your QR code..."):
            try:
                qr_image_bytes = generate_qr(data, box_size, border)
                
                # Display the image
                st.image(qr_image_bytes, caption="Your Generated QR Code", use_container_width=True)
                
                # Download button
                st.download_button(
                    label="💾 Download QR Code",
                    data=qr_image_bytes,
                    file_name="qrcode.png",
                    mime="image/png"
                )
                st.success("QR Code generated successfully!")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

st.markdown("---")
with st.expander("ℹ️ About this tool"):
    st.write("""
        This tool uses the `qrcode` library to generate standard QR codes. 
        It is built with Streamlit and is ready for deployment on **Streamlit Community Cloud**.
    """)
st.caption("Built with ❤️ using Streamlit")
