import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image, ImageEnhance

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


def generate_qr(
    data, box_size, border, fill_color, back_color,
    logo_image=None, rotation_angle=0,
    image_mode="Center Logo", bg_opacity=25,
):
    """Generates a QR code image with optional logo or background image."""
    # Use HIGH error correction when an image is present
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

    if logo_image and image_mode == "Background Image":
        # ── Background Image mode ────────────────────────────────────
        # Generate QR with black fill and white background first
        qr_img = qr.make_image(
            fill_color=fill_color, back_color="white"
        ).convert("RGBA")
        qr_w, qr_h = qr_img.size

        # Prepare the background image: resize to cover QR, apply opacity
        bg = logo_image.convert("RGBA").resize((qr_w, qr_h), Image.LANCZOS)

        # Rotate if requested
        if rotation_angle:
            bg = bg.rotate(rotation_angle, resample=Image.BICUBIC, expand=False)
            bg = bg.resize((qr_w, qr_h), Image.LANCZOS)

        # Lower the opacity of the background image
        alpha = bg.split()[3]
        alpha = alpha.point(lambda p: int(p * bg_opacity / 100))
        bg.putalpha(alpha)

        # Create a white canvas, paste the faded background image on it
        canvas = Image.new("RGBA", (qr_w, qr_h), (255, 255, 255, 255))
        canvas = Image.alpha_composite(canvas, bg)

        # Now make the QR's white pixels transparent so only dark modules remain
        qr_data = qr_img.getdata()
        transparent_qr = []
        for pixel in qr_data:
            # If pixel is white-ish (background), make it fully transparent
            if pixel[0] > 240 and pixel[1] > 240 and pixel[2] > 240:
                transparent_qr.append((0, 0, 0, 0))
            else:
                transparent_qr.append(pixel)
        qr_img.putdata(transparent_qr)

        # Composite: faded background + dark QR modules on top
        final = Image.alpha_composite(canvas, qr_img)

    else:
        # ── Normal / Center Logo mode ────────────────────────────────
        final = qr.make_image(
            fill_color=fill_color, back_color=back_color
        ).convert("RGBA")

        if logo_image and image_mode == "Center Logo":
            logo = logo_image.convert("RGBA")

            if rotation_angle:
                logo = logo.rotate(
                    rotation_angle, resample=Image.BICUBIC, expand=True
                )

            qr_w, qr_h = final.size
            max_logo_size = int(qr_w * 0.25)
            logo.thumbnail((max_logo_size, max_logo_size), Image.LANCZOS)

            logo_w, logo_h = logo.size
            pos = ((qr_w - logo_w) // 2, (qr_h - logo_h) // 2)
            final.paste(logo, pos, mask=logo)

    # Convert to bytes
    buf = BytesIO()
    final.save(buf, format="PNG")
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

st.sidebar.header("🖼️ Custom Image")
logo_file = st.sidebar.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg", "svg", "webp"],
    help="Use as a center logo or as a full background behind the QR code."
)

# Image options (only shown when an image is uploaded)
image_mode = "Center Logo"
rotation_angle = 0
bg_opacity = 25

if logo_file:
    image_mode = st.sidebar.radio(
        "Image Mode",
        ["Center Logo", "Background Image"],
        help="**Center Logo** — places the image in the center.\n\n"
             "**Background Image** — uses the image as a full background "
             "with adjustable opacity."
    )
    rotation_angle = st.sidebar.slider(
        "🔄 Rotate Image", min_value=0, max_value=360, value=0, step=15,
        help="Rotate the image before embedding."
    )
    if image_mode == "Background Image":
        bg_opacity = st.sidebar.slider(
            "🌫️ Background Opacity", min_value=5, max_value=50, value=25,
            step=5, help="Lower = more subtle, Higher = more visible."
        )
    st.sidebar.image(logo_file, caption="Image preview", use_container_width=True)

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
                logo_img = Image.open(logo_file) if logo_file else None

                qr_image_bytes = generate_qr(
                    data, box_size, border,
                    fill_color, back_color,
                    logo_image=logo_img,
                    rotation_angle=rotation_angle,
                    image_mode=image_mode,
                    bg_opacity=bg_opacity,
                )

                st.image(
                    qr_image_bytes,
                    caption="Your Generated QR Code",
                    use_container_width=True,
                )

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

        **Image Modes:**
        - **Center Logo** — places your image in the center of the QR code.
        - **Background Image** — uses the image as a full background with
          adjustable opacity (the white QR background is made transparent so
          the image shows through).

        Error correction is automatically raised to **HIGH** when an image is
        used, keeping the QR code scannable.

        Built with Streamlit and ready for deployment on
        **Streamlit Community Cloud**.
    """)
st.caption("Built with ❤️ using Streamlit")
