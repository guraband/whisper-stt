import whisper
import warnings
import time

# 경고 메시지 억제
warnings.filterwarnings("ignore", category=UserWarning,
                        message="FP16 is not supported on CPU; using FP32 instead")

try:
    # 모델 로드
    # model = whisper.load_model("base")
    model = whisper.load_model("small")

    start_time = time.time()

    # 음성 파일을 텍스트로 변환 (언어: 한국어)
    # result = model.transcribe("./resources/wav/reservation.mp3", language="ko")
    result = model.transcribe("./uploads/audio.wav", language="ko")

    end_time = time.time()

    processing_time = end_time - start_time

    # 결과 출력
    print(result["text"])
    print(f"Processing time: {processing_time:.2f} seconds")
except Exception as e:
    print(f"An error occurred: {e}")
