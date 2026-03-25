import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from cv_openrouter import CVAnalyzer

app = FastAPI()

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Global analyzer instance (for simplicity in local use)
analyzer = CVAnalyzer()
current_letter = ""

@app.post("/upload")
async def upload_files(cv: UploadFile = File(...), offer: UploadFile = File(...)):
    try:
        cv_path = os.path.join(UPLOAD_DIR, "cv.pdf")
        offer_path = os.path.join(UPLOAD_DIR, "offre.pdf")
        
        with open(cv_path, "wb") as buffer:
            shutil.copyfileobj(cv.file, buffer)
        with open(offer_path, "wb") as buffer:
            shutil.copyfileobj(offer.file, buffer)
            
        analyzer.prepare_data([cv_path, offer_path])
        return {"message": "Files uploaded and processed successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/generate")
async def generate_initial():
    global current_letter
    try:
        query = "Rédige une lettre de motivation complète et adaptée à l'offre en te basant sur mon CV."
        current_letter = analyzer.generate_letter(query)
        return {"letter": current_letter}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/modify")
async def modify_letter(prompt: str = Form(...)):
    global current_letter
    try:
        query = f"En te basant sur la lettre précédente : '{current_letter}', applique la modification suivante : {prompt}. Ne renvoie que le nouveau contenu de la lettre."
        current_letter = analyzer.generate_letter(query)
        return {"letter": current_letter}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/download")
async def download_pdf():
    try:
        output_path = "lettre_de_motivation.pdf"
        analyzer.export_pdf(current_letter, output_path)
        return FileResponse(output_path, media_type="application/pdf", filename="lettre_de_motivation.pdf")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Serve frontend
STATIC_DIR = os.path.join(BASE_DIR, "static")
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
