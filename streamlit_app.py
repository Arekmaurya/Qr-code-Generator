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


def generate_qr(data, box_size, border, fill_color, back_color, logo_image=None):
    """Generates a QR code image, optionally with a logo in the center."""
    # Use HIGH error correction when a logo is present so the QR stays scannable
    error_level = (
        qrcode.constants.ERROR_CORRECT_H
        if logo_image
        else qrcode.constants.ERROR_CORRECT_L
    )

    qr = qrcode.QRCode(
        version=1,
        error_correction=error_level,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")

    if logo_image:
        # Open and resize the logo
        logo = logo_image.convert("RGBA")

        # The logo should occupy at most ~25 % of the QR code area
        qr_width, qr_height = img.size
        max_logo_size = int(qr_width * 0.25)
        logo.thumbnail((max_logo_size, max_logo_size), Image.LANCZOS)

        # Center the logo
        logo_w, logo_h = logo.size
        pos = ((qr_width - logo_w) // 2, (qr_height - logo_h) // 2)

        # Paste with alpha mask so transparency is preserved
        img.paste(logo, pos, mask=logo)

    # Convert to bytes (use PNG to keep transparency)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


st.title("🖼️ QR Code Generator")
st.markdown(
    "Generate custom QR codes for your URLs, text, or location links instantly. "
    "Optimized for Streamlit Cloud."
)

# ── Sidebar ──────────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Configuration")
box_size = st.sidebar.slider(
    "Box Size", min_value=1, max_value=50, value=10,
    help="Size of each square in the QR code."
)
border = st.sidebar.slider(
    "Border Thickness", min_value=0, max_value=10, value=4,
    help="Thickness of the white border."
)

st.sidebar.header("🎨 Colors")
fill_color = st.sidebar.color_picker("QR Code Color", value="#000000")
back_color = st.sidebar.color_picker("Background Color", value="#FFFFFF")

st.sidebar.header("🖼️ Custom Logo / Image")
logo_file = st.sidebar.file_uploader(
    "Upload a logo to embed in the center",
    type=["png", "jpg", "jpeg", "svg", "webp"],
    help="The image will be resized and placed in the center of the QR code. "
         "Error correction is automatically increased to keep the QR scannable."
)

if logo_file:
    st.sidebar.image(logo_file, caption="Logo preview", use_container_width=True)

# ── Main input area ──────────────────────────────────────────────────────
data = st.text_area(
    "🔗 Enter Text or URL",
    placeholder="e.g., https://www.google.com",
    help="The content you want to encode in the QR code."
)

if st.button("Generate QR Code"):
    if not data:
        st.error("Please enter some data to generate a QR code.")
    else:
        with st.spinner("✨ Creating your QR code..."):
            try:
                # Load the logo if one was uploaded
                logo_img = Image.open(logo_file) if logo_file else None

                qr_image_bytes = generate_qr(
                    data, box_size, border,
                    fill_color, back_color,
                    logo_image=logo_img,
                )

                # Display the image
                st.image(
                    qr_image_bytes,
                    caption="Your Generated QR Code",
                    use_container_width=True,
                )

                # Download button
                st.download_button(
                    label="💾 Download QR Code",
                    data=qr_image_bytes,
                    file_name="qrcode.png",
                    mime="image/png",
                )
                st.success("QR Code generated successfully!")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

st.markdown("---")
with st.expander("ℹ️ About this tool"):
    st.write("""
        This tool uses the `qrcode` library to generate standard QR codes.
        You can optionally upload a **custom logo** that will be embedded in the
        center of the QR code. When a logo is added, error correction is
        automatically raised to **HIGH** so the code remains scannable.

        It is built with Streamlit and is ready for deployment on
        **Streamlit Community Cloud**.
    """)
st.caption("Built with ❤️ using Streamlit")
