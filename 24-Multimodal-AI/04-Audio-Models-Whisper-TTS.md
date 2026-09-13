# 04 - Audio Models: Whisper and TTS

## Prerequisites
- Sequence-to-Sequence Models
- Transformers and Attention Mechanism
- Basic Digital Signal Processing (Spectrograms, Mel-Frequency)

## Objectives
- Understand the architecture of Automatic Speech Recognition (ASR) models, focusing on OpenAI's Whisper.
- Learn about Text-to-Speech (TTS) models and vocoders.
- Explore the end-to-end processing pipeline for audio modalities.

## Intuition
Audio signals are continuous waveforms containing rich information: linguistic content, speaker identity, emotion, and background noise. Processing audio with deep learning typically involves transforming the 1D raw waveform into a 2D representation (Mel-spectrogram) that resembles an image, which can then be processed by CNNs or Transformers.

## Automatic Speech Recognition (ASR): OpenAI Whisper
Whisper is an encoder-decoder Transformer trained on 680,000 hours of multilingual and multitask supervised data.

### Pipeline
1. **Input**: Raw audio waveform resampled to 16kHz.
2. **Feature Extraction**: Converted to an 80-channel log-Mel spectrogram.
3. **Encoder**: A CNN stem processes the spectrogram, followed by Transformer encoder blocks. It learns to represent the audio features contextually.
4. **Decoder**: An autoregressive Transformer decoder predicts the text tokens.
5. **Multitask Format**: Whisper uses special tokens in the decoder prefix to specify the task (e.g., `<|startoftranscript|> <|en|> <|transcribe|>`) allowing a single model to do transcription, translation, and voice activity detection.

## Text-to-Speech (TTS)
TTS is the inverse of ASR: mapping text tokens to an audio waveform.
Modern TTS pipelines generally consist of two stages:
1. **Acoustic Model**: Maps text/phonemes to acoustic features (usually a Mel-spectrogram). Examples: Tacotron 2, FastSpeech.
2. **Vocoder**: Converts the Mel-spectrogram into a raw time-domain waveform. Examples: WaveNet, HiFi-GAN.

## Code Example: Transcribing Audio with Whisper

```python
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import soundfile as sf
import librosa

# Load Model and Processor
processor = WhisperProcessor.from_pretrained("openai/whisper-tiny.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny.en")

# Load dummy audio (using librosa to resample to 16kHz if needed)
# In practice, replace with a real audio file path
# audio, rate = librosa.load("sample.wav", sr=16000)
audio = torch.randn(16000 * 3) # 3 seconds of white noise for demonstration

# Process input
input_features = processor(audio, sampling_rate=16000, return_tensors="pt").input_features

# Generate token ids
predicted_ids = model.generate(input_features)

# Decode tokens to text
transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
print("Transcription:", transcription[0])
```

## Interview Questions
1. **Q: Why do audio models like Whisper use log-Mel spectrograms instead of raw waveforms as input?**
   **A**: Log-Mel spectrograms map frequencies to a Mel scale that mimics human auditory perception, compressing redundant information and making it easier for models to extract phonetically relevant features compared to high-dimensional, noisy raw waveforms.
2. **Q: What is the role of a vocoder in a TTS system?**
   **A**: An acoustic model generates a spectrogram (which lacks phase information), and the vocoder's job is to reconstruct the phase and generate a high-fidelity raw audio waveform from that spectrogram.
