import whisper
import time
from lightning_whisper_mlx import LightningWhisperMLX

# whisper 대신 LightningWhisperMLX를 사용하여 테스트
try:
    whisper = LightningWhisperMLX(model="small", batch_size=12, quant=None)

    audio_files = [
        "./resources/wav/hello.mp3",
        "./resources/wav/audio.wav",
        "./resources/wav/output_1m.wav",
        "./resources/wav/output_4m.wav",
        "./resources/wav/output_13m.wav",
    ]

    total_start_time = time.time()
    for audio_file in audio_files:
        start_time = time.time()

        result = whisper.transcribe(audio_file, language="ko")

        end_time = time.time()

        processing_time = end_time - start_time

        # 결과 출력
        # print audio file name strip off the path
        print(f"Audio file: {audio_file.split('/')[-1]}")
        print(result["text"])
        print(f"Processing time: {processing_time:.2f} seconds")
        print()
    print(
        f"Total processing time: {(time.time() - total_start_time):.2f} seconds")
    print()
except Exception as e:
    print(f"An error occurred: {e}")
