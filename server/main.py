from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import whisper
from lightning_whisper_mlx import LightningWhisperMLX
import uvicorn
import logging
import os
import time
import aiofiles
import uuid
import similarity
import random
import json

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
model2 = LightningWhisperMLX(model="small", batch_size=12, quant=None)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Directory to save uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...), 
    model_type: str = Form('lightning'), 
    language: str = Form('en'),
    sentence_id: int = Form(...)
):
    logging.info(f"Received file: {file.filename}")
    logging.info(f"Model: {model_type}")
    logging.info(f"Language: {language}")
    logging.info(f"Sentence ID: {sentence_id}")

    # Generate a unique file name using UUID
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_location = os.path.join(UPLOAD_DIR, unique_filename)

    # Save the uploaded file asynchronously
    async with aiofiles.open(file_location, "wb") as f:
        content = await file.read()
        await f.write(content)

    # Whisper 모델을 사용하여 텍스트로 변환
    start_time = time.time()

    if model_type == "whisper":
        logging.info(f"Model1: {model_type}")
        result = model.transcribe(file_location, language=language)
    else:
        logging.info(f"Model2: {model_type}")
        result = model2.transcribe(file_location, language=language)

    end_time = time.time()

    processing_time = end_time - start_time
    logging.info(f"Transcription result: {result}")
    logging.info(f"Processing time: {processing_time:.2f} seconds")

    # Find the original sentence text
    with open(os.path.join(os.path.dirname(__file__), "../resources/json/sentence.json"), "r") as f:
        sentences = json.load(f)
    original_sentence = next((s['text'] for s in sentences if s['id'] == sentence_id), "Unknown sentence")

    # Calculate similarity score
    similarity_score = similarity.calculate_similarity(result["text"], original_sentence)

    print(f"Original sentence: {original_sentence}")
    print(f"Transcribed text: {result['text']}")
    print(f"Similarity score: {similarity_score}")

    return JSONResponse(content={
        "text": result["text"], 
        "original_sentence": original_sentence,
        "similarity_score": similarity_score
    })


@app.get("/random_sentence")
async def random_sentence():
    with open(os.path.join(os.path.dirname(__file__), "../resources/json/sentence.json"), "r") as f:
        sentences = json.load(f)
    sentence = random.choice(sentences)
    file_path = os.path.join(os.path.dirname(__file__), "../resources/sentences", sentence["file"])
    return JSONResponse(content={"sentence": sentence, "file_path": file_path})

@app.get("/play_audio")
async def play_audio(file_path: str):
    return FileResponse(file_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
