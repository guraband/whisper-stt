### 가상환경 생성
python -m venv venv

### 가상환경 활성화
source venv/bin/activate

### alias 설정
alias python=python3
alias pip=pip3

### 가상환경 비활성화
deactivate

### requirements.txt 생성
```sh
pip freeze > requirements.txt
```

### requirements.txt 실행
```sh
pip install -r requirements.txt
```

### 음성 wav 파일 생성
https://luvvoice.com/kr

### Whisper AI 설치 (MacBook M1)
1. Homebrew 설치 (이미 설치된 경우 건너뛰기)
```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. FFmpeg 설치
```sh
brew install ffmpeg
```

3. Whisper 설치
```sh
pip install git+https://github.com/openai/whisper.git
```

4. PyTorch 설치 (Apple Silicon 전용)
```sh
pip install torch torchaudio
```

5. Whisper 사용 예제
```python
import whisper

model = whisper.load_model("base")
result = model.transcribe("audio.mp3")
print(result["text"])
```

### coreML 설치
```sh
pip install coremltools
```
