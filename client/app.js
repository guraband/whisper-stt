const recordButton = document.getElementById('recordButton');
const stopButton = document.getElementById('stopButton');
const transcription = document.getElementById('transcription');
const canvas = document.getElementById('visualizer');
const canvasCtx = canvas.getContext('2d');
const loading = document.getElementById('loading');

let mediaRecorder;
let audioChunks = [];
let silenceTimeout;
let audioContext;
let analyser;
let dataArray;
let bufferLength;

const SILENCE_DURATION = 2000; // 2 seconds
const SILENCE_THRESHOLD = 1; // Threshold for detecting silence

recordButton.addEventListener('click', () => {
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

                const selectedModel = document.querySelector('input[name="model"]:checked').value;
                formData.append('model_type', selectedModel);

                transcription.textContent = ''; // Clear previous result
                showLoading();
                const startTime = performance.now();
                fetch('http://localhost:8000/transcribe', {
                    method: 'POST',
                    body: formData
                })
                    .then(response => response.json())
                    .then(data => {
                        const endTime = performance.now();
                        const processingTime = ((endTime - startTime) / 1000).toFixed(2);
                        transcription.textContent = `결과: ${data.text}\n 처리시간: ${processingTime} seconds`;
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    })
                    .finally(() => {
                        hideLoading();
                    });

                audioChunks = [];
                audioContext.close();
            });

            recordButton.disabled = true;
            stopButton.disabled = false;
            resetSilenceTimeout();
            drawVisualizer();
        });
});

stopButton.addEventListener('click', () => {
    stopRecording();
});

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
    }
    recordButton.disabled = false;
    stopButton.disabled = true;
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

function showLoading() {
    loading.style.display = 'block';
}

function hideLoading() {
    loading.style.display = 'none';
}
