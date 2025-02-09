async function fetchRandomSentence() {
    const response = await fetch('http://localhost:8000/random_sentence');
    const data = await response.json();
    document.getElementById('sentence-text').innerText = data.sentence.text;
    document.getElementById('sentence-audio').src = `http://localhost:8000/play_audio?file_path=${encodeURIComponent(data.file_path)}`;
    document.getElementById('sentence-text').style.display = 'none';
    document.getElementById('sentence-text').dataset.id = data.sentence.id; // Store sentence ID
}

function clearSentence() {
    document.getElementById('sentence-text').innerText = '';
    document.getElementById('sentence-audio').src = '';
    clearResult();
}

function clearResult() {
    document.getElementById('transcription-result').innerText = '';
    document.getElementById('similarity-score').innerText = '';
    document.getElementById('success-message').innerText = '';
}

function showLoading() {
    document.getElementById('loading').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function disableButtons() {
    document.getElementById('listen-button').disabled = true;
    document.getElementById('try-button').disabled = true;
    document.getElementById('show-text-button').disabled = true;
    document.getElementById('next-button').disabled = true;
}

function enableButtons() {
    document.getElementById('listen-button').disabled = false;
    document.getElementById('try-button').disabled = false;
    document.getElementById('show-text-button').disabled = false;
    document.getElementById('next-button').disabled = false;
}

document.addEventListener('DOMContentLoaded', () => {
    fetchRandomSentence();
    document.getElementById('next-button').addEventListener('click', () => {
        clearSentence();
        fetchRandomSentence().then(() => {
            const audioElement = document.getElementById('sentence-audio');
            audioElement.addEventListener('loadeddata', () => {
                audioElement.play();
            });
        });
        document.getElementById('try-button').innerText = 'Try 🎤';
    });
    document.getElementById('listen-button').addEventListener('click', () => {
        document.getElementById('sentence-audio').play();
    });
    document.getElementById('show-text-button').addEventListener('click', () => {
        document.getElementById('sentence-text').style.display = 'block';
    });
    document.getElementById('try-button').addEventListener('click', () => {
        const tryButton = document.getElementById('try-button');
        if (tryButton.innerText === 'Recording 🎙️') {
            stopRecording();
        } else {
            tryButton.innerText = 'Recording 🎙️';
            startRecording();
        }
    });
});

let mediaRecorder;
let audioChunks = [];
let silenceTimeout;
let audioContext;
let analyser;
let dataArray;
let bufferLength;
const canvas = document.getElementById('visualizer');
const canvasCtx = canvas.getContext('2d');

const SILENCE_DURATION = 2000; // 2 seconds
const SILENCE_THRESHOLD = 1; // Threshold for detecting silence

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const source = audioContext.createMediaStreamSource(stream);
            analyser = audioContext.createAnalyser();
            source.connect(analyser);
            analyser.fftSize = 2048;
            bufferLength = analyser.frequencyBinCount;
            dataArray = new Uint8Array(bufferLength);

            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            mediaRecorder.addEventListener('dataavailable', event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener('stop', () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const formData = new FormData();
                formData.append('file', audioBlob, 'audio.wav');

                const selectedModel = 'whisper'; // Default model
                formData.append('model_type', selectedModel);

                const selectedLanguage = 'en'; // Default language
                formData.append('language', selectedLanguage);

                const sentenceId = document.getElementById('sentence-text').dataset.id; // Get sentence ID
                formData.append('sentence_id', sentenceId);

                showLoading();
                disableButtons();

                fetch('http://localhost:8000/transcribe', {
                    method: 'POST',
                    body: formData
                })
                    .then(response => response.json())
                    .then(data => {
                        const similarityScore = data.similarity_score * 100; // Convert to percentage
                        document.getElementById('transcription-result').innerText = `Transcription: ${data.text}`;
                        document.getElementById('similarity-score').innerText = `Similarity Score: ${similarityScore}%`;
                        if (similarityScore >= 85) {
                            document.getElementById('success-message').innerText = "Success";
                            document.getElementById('success-message').style.color = '#28a745';
                        } else {
                            document.getElementById('success-message').innerText = "Try Again";
                            document.getElementById('success-message').style.color = '#dc3545';
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    })
                    .finally(() => {
                        hideLoading();
                        enableButtons();
                    });

                audioChunks = [];
                audioContext.close();
            });

            resetSilenceTimeout();
            drawVisualizer();
        });
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
    }
    document.getElementById('try-button').innerText = 'Try 🎤';
    clearTimeout(silenceTimeout);
}

function resetSilenceTimeout() {
    clearTimeout(silenceTimeout);
    silenceTimeout = setTimeout(() => {
        stopRecording();
    }, SILENCE_DURATION);
}

function drawVisualizer() {
    requestAnimationFrame(drawVisualizer);

    analyser.getByteTimeDomainData(dataArray);

    canvasCtx.fillStyle = 'rgb(255, 255, 255)';
    canvasCtx.fillRect(0, 0, canvas.width, canvas.height);

    canvasCtx.lineWidth = 2;
    canvasCtx.strokeStyle = 'rgb(0, 123, 255)';

    canvasCtx.beginPath();

    const sliceWidth = canvas.width * 1.0 / bufferLength;
    let x = 0;
    let isSilent = true;

    for (let i = 0; i < bufferLength; i++) {
        const v = dataArray[i] / 128.0;
        const y = v * canvas.height / 2;

        if (v > SILENCE_THRESHOLD) {
            isSilent = false;
        }

        if (i === 0) {
            canvasCtx.moveTo(x, y);
        } else {
            canvasCtx.lineTo(x, y);
        }

        x += sliceWidth;
    }

    canvasCtx.lineTo(canvas.width, canvas.height / 2);
    canvasCtx.stroke();

    if (!isSilent) {
        resetSilenceTimeout();
    }
}
