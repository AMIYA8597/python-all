"""
# ==============================================================================
# LABORATORY: DIGITAL SIGNAL PROCESSING (SCIPY.SIGNAL)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# When dealing with real-world sensors (Audio Microphones, ECG Heart Monitors, 
# Radio Telescopes, or Stock Market prices), the data is never a perfect, clean 
# mathematical line. It is heavily corrupted by "Noise" (static, electrical 
# interference, random variance).
#
# Digital Signal Processing (DSP) is the mathematical science of manipulating 
# these raw signals.
#
# With `scipy.signal` and `scipy.fft` (Fast Fourier Transform), we can:
# 1. Mathematically dissect a signal to find its hidden frequencies.
# 2. Design Digital Filters (like a Low-Pass Butterworth filter) to permanently 
#    erase the high-frequency static noise while leaving the true signal intact!
# 3. Use Convolution to blend signals together.
#
# This is how Noise-Canceling Headphones work, how MP3 audio compression works, 
# and how self-driving cars clean their LiDAR sensor data!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Time Domain vs. Frequency Domain.
# - Apply the Fast Fourier Transform (FFT) to find hidden frequencies.
# - Design and apply a Butterworth Low-Pass Filter to erase static noise.
#
# ==============================================================================
"""

import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. GENERATING A NOISY SIGNAL
# ==============================================================================
def create_noisy_signal():
    """
    Simulates a heart monitor (ECG) or a clean audio tone that has been 
    severely corrupted by electrical static noise.
    """
    # 1. Time Array: 1000 samples per second, for 1 second.
    sample_rate = 1000
    t = np.linspace(0, 1.0, sample_rate, endpoint=False)
    
    # 2. THE TRUE SIGNAL (e.g., A clean, low 5 Hz wave)
    true_signal = np.sin(2 * np.pi * 5 * t)
    
    # 3. THE NOISE (e.g., A harsh, high-pitched 50 Hz electrical hum)
    # Plus some completely random white noise!
    electrical_hum = 0.5 * np.sin(2 * np.pi * 50 * t)
    white_noise = np.random.normal(0, 0.3, len(t))
    
    # The final corrupted signal received by the computer
    corrupted_signal = true_signal + electrical_hum + white_noise
    
    return t, corrupted_signal, sample_rate


# ==============================================================================
# 4. FAST FOURIER TRANSFORM (FFT)
# ==============================================================================
def demonstrate_fft(t, corrupted_signal, sample_rate):
    section_header("Fast Fourier Transform (Finding Hidden Frequencies)")
    
    # Looking at the raw `corrupted_signal` array, it just looks like a chaotic 
    # mess of random numbers (The Time Domain).
    
    # The FFT mathematically converts the Time Domain into the Frequency Domain!
    # It decomposes the chaotic signal into the exact fundamental sine waves 
    # that created it!
    
    n = len(corrupted_signal)
    
    # Execute the FFT! (Returns complex numbers)
    yf = fft(corrupted_signal)
    
    # Get the corresponding X-axis frequencies
    xf = fftfreq(n, 1 / sample_rate)
    
    # We only care about the positive frequencies (first half of the array)
    positive_freqs = xf[:n//2]
    amplitudes = np.abs(yf[:n//2])
    
    # Let's find the top 2 strongest frequencies in the corrupted signal!
    # We sort the indices by amplitude in descending order.
    top_indices = np.argsort(amplitudes)[::-1][:2]
    
    print("The FFT analyzed the chaotic noise and found two dominant spikes:")
    for idx in top_indices:
        freq = positive_freqs[idx]
        amp = amplitudes[idx]
        print(f" - Found Frequency: {freq:>4.1f} Hz (Amplitude: {amp:.0f})")
        
    print("\nNotice how the FFT perfectly identified our 5 Hz true signal AND ")
    print("our 50 Hz electrical hum, completely ignoring the white noise!")


# ==============================================================================
# 5. DIGITAL FILTERING (BUTTERWORTH)
# ==============================================================================
def demonstrate_filtering(t, corrupted_signal, sample_rate):
    section_header("Digital Filtering (Erasing the Noise)")
    
    # Now that the FFT told us the noise is living at 50 Hz and above, we can 
    # build a "Low-Pass Filter". This acts like a bouncer at a club: 
    # It allows low frequencies (like our 5 Hz signal) to pass through, but 
    # permanently deletes any frequency higher than the cutoff!
    
    cutoff_frequency = 15.0 # Hz (Erase everything above 15 Hz)
    
    # The Nyquist Frequency is exactly half the sample rate. 
    # SciPy filters require the cutoff to be normalized against the Nyquist frequency.
    nyquist = 0.5 * sample_rate
    normalized_cutoff = cutoff_frequency / nyquist
    
    # 1. DESIGN THE FILTER (Butterworth)
    # Order=4 controls how "sharp" the cutoff cliff is.
    b, a = signal.butter(N=4, Wn=normalized_cutoff, btype='low', analog=False)
    
    # 2. APPLY THE FILTER
    # `filtfilt` applies the filter forwards and then backwards. This guarantees 
    # "Zero Phase Shift" (meaning the filtered signal won't be artificially 
    # delayed in time compared to the original signal).
    clean_signal = signal.filtfilt(b, a, corrupted_signal)
    
    print(f"Filter created: Low-Pass at {cutoff_frequency} Hz.")
    print("Filter applied to the corrupted signal.")
    
    # Let's evaluate the cleaning!
    # We'll calculate the Variance (amount of chaos) in the signals.
    print(f"\nCorrupted Signal Variance: {np.var(corrupted_signal):.4f}")
    print(f"Cleaned Signal Variance  : {np.var(clean_signal):.4f}")
    print("The variance dropped massively because the high-frequency static was erased!")
    print("The `clean_signal` is now a beautiful, smooth 5 Hz sine wave.")


def run_all_labs():
    t, corrupted, sr = create_noisy_signal()
    demonstrate_fft(t, corrupted, sr)
    demonstrate_filtering(t, corrupted, sr)


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental difference between the Time Domain and the Frequency Domain?
   Answer: The Time Domain shows how a signal changes over time (X-axis is Seconds, Y-axis is Amplitude). An audio file is in the Time Domain. The Frequency Domain shows what mathematical ingredients (sine waves) make up the signal (X-axis is Hertz/Pitch, Y-axis is Strength/Volume). A Graphic Equalizer on a stereo system shows the Frequency Domain. The FFT is the mathematical bridge that converts Time Domain into Frequency Domain.

2. Why do we normalize the cutoff frequency against the Nyquist Frequency?
   Answer: The Nyquist-Shannon Sampling Theorem states that a digital system can only accurately record a frequency if it samples it at least TWICE per cycle. If your microphone samples at 1000 Hz, the absolute highest pitch it can physically record without aliasing is 500 Hz (The Nyquist Frequency). Because SciPy filters are designed to work abstractly, regardless of your hardware, they require you to define the cutoff as a ratio between 0.0 and 1.0, where 1.0 represents the absolute physical limit of your hardware (Nyquist).

3. Why use `filtfilt` instead of `lfilter`?
   Answer: When you push an array of data through a mathematical filter (`lfilter`), the mathematics inherently cause a "Phase Delay". The resulting clean sine wave will be shifted slightly to the right (delayed in time). In a self-driving car, a delayed sensor reading is fatal. `filtfilt` runs the data through the filter forwards, and then immediately runs it backwards! The backwards pass perfectly cancels out the mathematical delay of the forward pass, resulting in "Zero-Phase Filtering" (the clean signal aligns perfectly in time with the original).
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Digital Signal Processing Completed.")
