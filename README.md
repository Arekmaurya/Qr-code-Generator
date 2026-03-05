# 🖼️ QR Code Generator

A powerful and sleek QR Code Generator built with **FastAPI** and **Streamlit**. Generate custom QR codes for URLs, text, or location links instantly.

## 🚀 Live Demo
Check out the live application here:  
**[👉 Live Demo on Streamlit Cloud](https://qr-code-generator-harsh.streamlit.app/)**

---

## ✨ Features
- **Instant Generation**: Get your QR code in seconds.
- **Customizable**: Adjust box size and border thickness.
- **Downloadable**: Save your generated QR codes as high-quality PNG images.
- **Dual Architecture**:
    - **FastAPI Backend**: Robust API for programmatic QR generation.
    - **Streamlit Frontend**: Beautiful, interactive user interface.
- **Cloud Ready**: Optimized for deployment on Streamlit Community Cloud.
- **Docker Support**: Containerized for easy sharing and deployment.

---

## 🛠️ Technology Stack
- **Backend**: FastAPI, Python
- **Frontend**: Streamlit
- **QR Engine**: `qrcode` library with `Pillow` (PIL)
- **Validation**: Pydantic
- **Deployment**: Docker, Streamlit Cloud

---

## 💻 Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/Arekmaurya/Qr-code-Generator.git
cd Qr-code-Generator
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
You have two options for running locally:

#### Option A: Standalone Streamlit (Recommended for quick use)
This runs the integrated version optimized for the cloud.
```bash
streamlit run streamlit_app.py
```

#### Option B: Full Stack (FastAPI + Streamlit)
1. Start the backend:
   ```bash
   python main.py
   ```
2. Start the frontend:
   ```bash
   streamlit run app.pystreamlit
   ```

---

## 🐳 Docker Deployment
Run the entire stack with a single command:
```bash
docker-compose up --build
```
- **Frontend**: `http://localhost:8501`
- **Backend API**: `http://localhost:8000`

---

## 📄 License
This project is open-source and available under the MIT License.

Built with ❤️ by [Arekmaurya](https://github.com/Arekmaurya)
