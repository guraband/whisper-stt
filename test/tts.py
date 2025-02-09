from TTS.api import TTS
import time

# 사용할 모델 선택
model_name = "tts_models/en/ljspeech/tacotron2-DDC"  # 또는 "tts_models/en/ljspeech/fast_pitch"

# 모델 로드
tts = TTS(model_name).to("cpu")

# 음성 파일로 저장

# 문장들
texts = [
    "I'm running a little late, but I'll be there in about ten minutes.",
    "Could you recommend a good restaurant around here that serves local food?",
    "I was planning to stay home this weekend, but now I’m thinking about going on a short trip.",
    "I need to get some rest because I have an important meeting early in the morning.",
    "I really enjoyed the movie last night, especially the twist at the end.",
    "Would you mind turning down the volume a little? It’s a bit too loud for me.",
    "I’ve been trying to eat healthier, so I’m avoiding fast food these days.",
    "Even though I was really tired, I stayed up late to finish my work.",
    "I don’t know much about technology, but I’d love to learn more about it.",
    "If you ever need any help, just let me know and I’ll do my best to assist you.",
]

for i, text in enumerate(texts):
    start_time = time.time()
    print(f"Processing sentence {i+1}/{len(texts)}")
    tts.tts_to_file(text=text, file_path=f"./resources/sentences/sentence_{i+1}.wav")
    print(f"processing time: {(time.time() - start_time):.2f} seconds\n")
