from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import whisper
import uvicorn
import logging
import os
import time

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

model = whisper.load_model("small")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Directory to save uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    logging.info(f"Received file: {file.filename}")

    # Save the uploaded file
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Load the audio file
    try:
        audio = whisper.load_audio(file_location)
    except Exception as e:
        logging.error(f"Error reading audio file: {e}")
        raise HTTPException(status_code=400, detail="Invalid audio format")

    # Whisper 모델을 사용하여 텍스트로 변환
    start_time = time.time()
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    options = whisper.DecodingOptions(language="ko")
    result = whisper.decode(model, mel, options)
    end_time = time.time()

    processing_time = end_time - start_time
    logging.info(f"Transcription result: {result.text}")
    logging.info(f"Processing time: {processing_time:.2f} seconds")

    return JSONResponse(content={"text": result.text})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
