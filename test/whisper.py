import whisper
import warnings
import time

# 경고 메시지 억제
warnings.filterwarnings("ignore", category=UserWarning,
                        message="FP16 is not supported on CPU; using FP32 instead")

try:
    # 모델 로드
    model = whisper.load_model("small")

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

        # 음성 파일을 텍스트로 변환 (언어: 한국어)
        # result = model.transcribe("./resources/wav/reservation.mp3", language="ko")
        result = model.transcribe(audio_file, language="ko")

        end_time = time.time()

        processing_time = end_time - start_time

        # 결과 출력
        print(f"Audio file: {audio_file.split('/')[-1]}")
        print(result["text"])
        print(f"Processing time: {processing_time:.2f} seconds")
        print()
    print(
        f"Total processing time: {(time.time() - total_start_time):.2f} seconds")
    print()
except Exception as e:
    print(f"An error occurred: {e}")
