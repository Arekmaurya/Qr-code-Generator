import io
import qrcode
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

# Initialize FastAPI app
app = FastAPI(
    title="QR Code Generator API",
    description="A simple API to generate QR codes from text or URLs.",
    version="1.0.0"
)

# Input model for validation
class QRCodeRequest(BaseModel):
    data: str = Field(..., min_length=1, description="The text or URL to encode in the QR code.")
    box_size: Optional[int] = Field(10, ge=1, le=50, description="Size of each box in the QR code grid.")
    border: Optional[int] = Field(4, ge=0, le=10, description="Thickness of the border.")

@app.get("/")
async def root():
    """Root endpoint to check API status."""
    return {"message": "Welcome to the QR Code Generator API. Visit /docs for documentation."}

@app.post("/generate")
async def generate_qr(request: QRCodeRequest):
    """
    Generate a QR code image from the provided data.
    
    - **data**: The string or URL to encode.
    - **box_size**: Optional grid size (default: 10).
    - **border**: Optional border thickness (default: 4).
    """
    try:
        # Initialize QR Code object
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=request.box_size,
            border=request.border,
        )
        
        # Add data to the QR code
        qr.add_data(request.data)
        qr.make(fit=True)

        # Create the image using Pillow
        img = qr.make_image(fill_color="black", back_color="white")

        # Save image to a bytes buffer
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        # Return the image as a streaming response
        return StreamingResponse(buf, media_type="image/png")

    except Exception as e:
        # Generic error handling
        raise HTTPException(status_code=500, detail=f"Failed to generate QR code: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
