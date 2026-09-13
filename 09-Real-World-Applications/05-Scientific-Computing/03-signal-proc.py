\"\"\"
Scientific Computing in Python: Signal Processing

What is Signal Processing?
--------------------------
Signal processing is the analysis, synthesis, and modification of signals, which are broadly defined as functions conveying information about the behavior or attributes of some phenomenon. In the real world, signals can be audio, video, seismic data, medical readings (like ECG or EEG), or financial time series.

Why does it exist?
------------------
Raw data is often noisy, incomplete, or contains multiple overlapping sources of information. Signal processing exists to:
1. Extract useful information (e.g., finding the fundamental frequency of a sound).
2. Remove unwanted noise (e.g., smoothing out high-frequency sensor noise).
3. Transform signals into a more useful domain (e.g., time domain to frequency domain via Fourier Transforms).

Industry Use Cases:
-------------------
- Telecommunications: Encoding and decoding transmissions, noise filtering.
- Audio Engineering: Equalization, compression, pitch correction.
- Medical Imaging/Devices: MRI reconstruction, heart rate monitoring from ECGs.
- Finance: Algorithmic trading via moving average filters and trend extraction.
- Geophysics: Analyzing seismic data to find oil and gas.

Beginner Explanation:
---------------------
Imagine you are at a crowded party trying to listen to your friend. The sound reaching your ears is a mixture of your friend's voice, background music, and other people talking. Signal processing is like your brain's ability to "tune out" the background noise and focus on your friend. In code, we use mathematical operations to achieve this filtering.

Advanced Technical Explanation:
-------------------------------
Continuous signals $x(t)$ are sampled to create discrete signals $x[n]$. The core of digital signal processing (DSP) relies on Linear Time-Invariant (LTI) systems, which can be fully characterized by their impulse response $h[n]$. The output of an LTI system is the convolution of the input signal with the impulse response: $y[n] = x[n] * h[n]$. 
The Z-transform and the Discrete Fourier Transform (DFT) (efficiently implemented as the Fast Fourier Transform, FFT) are crucial for analyzing these systems in the frequency domain. Designing a digital filter involves placing poles and zeros in the complex Z-plane to shape the frequency response.

Practical Examples Included:
1. Generating a noisy signal.
2. Filtering the noise using a Butterworth Low-Pass Filter.
3. Analyzing the frequency components using Fast Fourier Transform (FFT).
4. Finding peaks in a signal.

Performance Considerations:
---------------------------
- Convolution in the time domain is $O(N^2)$ for large arrays, but using the FFT reduces this to $O(N \log N)$ (Fast Convolution).
- Vectorized operations via NumPy and optimized routines in `scipy.signal` avoid Python loop overhead.

Security Concerns:
------------------
- When processing signals from untrusted sources, be cautious of buffer overflows if the DSP library isn't memory-safe (though NumPy/SciPy are generally robust).
- Adversarial signals can be designed to exploit edge cases in classification algorithms downstream (e.g., adversarial audio).

Interview Questions:
--------------------
1. What is the difference between a Finite Impulse Response (FIR) and an Infinite Impulse Response (IIR) filter?
   *Answer: FIR filters only depend on current and past inputs, meaning they are always stable and can have perfectly linear phase. IIR filters depend on past inputs and past outputs (feedback), meaning they can be unstable but typically require lower order (less computation) to achieve the same frequency response cutoff.*
2. Why do we use window functions before computing an FFT?
   *Answer: When taking an FFT of a finite segment of an infinite signal, the truncation causes "spectral leakage". Windowing tapers the ends of the segment to zero, reducing the abrupt discontinuities at the boundaries and minimizing this leakage.*

Practical Exercises:
--------------------
1. Generate a square wave and a sawtooth wave, then analyze their harmonic content using FFT.
2. Design an IIR Band-Pass filter to isolate a specific frequency from a sum of sine waves.
3. Use `scipy.signal.spectrogram` to plot the time-varying frequency content of a "chirp" signal.
\"\"\"

import numpy as np
import scipy.signal as signal
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

def generate_signal(duration=1.0, sample_rate=1000):
    \"\"\"
    Generates a synthetic signal: a 5 Hz sine wave + a 50 Hz sine wave + Gaussian noise.
    
    Args:
        duration (float): Length of signal in seconds.
        sample_rate (int): Number of samples per second.
        
    Returns:
        tuple: (time_array, signal_array)
    \"\"\"
    # Time array: from 0 to duration, with `sample_rate` steps per second
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # 5 Hz low-frequency component (e.g., the signal we want)
    signal_5hz = np.sin(2 * np.pi * 5 * t)
    
    # 50 Hz high-frequency component (e.g., power line interference)
    signal_50hz = 0.5 * np.sin(2 * np.pi * 50 * t)
    
    # Random Gaussian noise
    noise = 0.3 * np.random.normal(size=t.shape)
    
    # Combine everything
    combined_signal = signal_5hz + signal_50hz + noise
    
    return t, combined_signal


def apply_lowpass_filter(data, cutoff_freq, sample_rate, order=4):
    \"\"\"
    Applies a Butterworth low-pass filter to the data.
    
    Args:
        data (np.ndarray): The signal data.
        cutoff_freq (float): The frequency above which signals are attenuated.
        sample_rate (int): The sampling rate of the data.
        order (int): The order of the filter (higher = steeper roll-off).
        
    Returns:
        np.ndarray: The filtered signal.
    \"\"\"
    # Nyquist frequency is half the sample rate
    nyquist = 0.5 * sample_rate
    
    # Normalize cutoff frequency to Nyquist (required by scipy.signal)
    normal_cutoff = cutoff_freq / nyquist
    
    # Design the Butterworth filter
    # b = numerator coefficients, a = denominator coefficients of the IIR filter
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    
    # Apply the filter using filtfilt (zero-phase filtering, meaning no delay is introduced)
    filtered_data = signal.filtfilt(b, a, data)
    
    return filtered_data


def analyze_frequency_content(data, sample_rate):
    \"\"\"
    Computes the Fast Fourier Transform (FFT) of the signal to find its frequency components.
    
    Args:
        data (np.ndarray): The signal data.
        sample_rate (int): The sampling rate.
        
    Returns:
        tuple: (frequencies, power_spectrum)
    \"\"\"
    N = len(data)
    
    # Compute the 1D discrete Fourier Transform
    # We use fft() which implements the FFT algorithm efficiently
    yf = fft(data)
    
    # Generate the corresponding frequencies for the x-axis
    xf = fftfreq(N, 1 / sample_rate)
    
    # We take the absolute value to get magnitude and square it to get power.
    # We only care about positive frequencies, which are the first half of the array.
    power_spectrum = np.abs(yf[:N//2]) ** 2
    positive_frequencies = xf[:N//2]
    
    return positive_frequencies, power_spectrum


def find_signal_peaks(data, distance=None, prominence=None):
    \"\"\"
    Finds local maxima (peaks) in a signal.
    
    Args:
        data (np.ndarray): The signal data.
        distance (int): Minimal horizontal distance in samples between peaks.
        prominence (float): Minimum prominence of peaks.
        
    Returns:
        np.ndarray: Indices of the peaks.
    \"\"\"
    # find_peaks relies on local topographic properties. 
    # Prominence measures how much a peak stands out from its baseline.
    peaks, _ = signal.find_peaks(data, distance=distance, prominence=prominence)
    return peaks


if __name__ == "__main__":
    print("Starting Signal Processing Demonstration...")
    
    # 1. Generate Data
    fs = 1000 # 1000 Hz sample rate
    t, raw_sig = generate_signal(duration=2.0, sample_rate=fs)
    print(f"Generated signal of length {len(raw_sig)}")
    
    # 2. Filter Data
    # We want to keep the 5Hz signal and remove the 50Hz noise + random noise.
    # So we set a cutoff around 15Hz.
    filtered_sig = apply_lowpass_filter(raw_sig, cutoff_freq=15.0, sample_rate=fs, order=4)
    print("Applied Butterworth Low-Pass Filter")
    
    # 3. Analyze Frequencies
    freqs_raw, power_raw = analyze_frequency_content(raw_sig, fs)
    freqs_filt, power_filt = analyze_frequency_content(filtered_sig, fs)
    print("Computed Fast Fourier Transforms")
    
    # 4. Find Peaks in filtered signal
    # Distance of 100 samples (0.1s at 1000Hz) ensures we don't pick up tiny bumps
    peaks = find_signal_peaks(filtered_sig, distance=100, prominence=0.5)
    print(f"Found {len(peaks)} prominent peaks in the filtered signal.")

    print("\nDemonstration complete! Run this script in an environment with matplotlib to visualize (visualization code is commented out below).")
    
    # Visualization block (uncomment if you want to plot)
    \"\"\"
    plt.figure(figsize=(12, 8))
    
    # Plot Time Domain
    plt.subplot(2, 1, 1)
    plt.plot(t, raw_sig, label='Noisy Raw Signal', alpha=0.5)
    plt.plot(t, filtered_sig, label='Filtered Signal (5Hz)', linewidth=2)
    plt.plot(t[peaks], filtered_sig[peaks], "x", color='red', markersize=10, label='Detected Peaks')
    plt.title('Time Domain Analysis')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    
    # Plot Frequency Domain
    plt.subplot(2, 1, 2)
    plt.plot(freqs_raw, power_raw, label='Raw Spectrum', alpha=0.5)
    plt.plot(freqs_filt, power_filt, label='Filtered Spectrum')
    plt.title('Frequency Domain Analysis (FFT)')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Power')
    plt.xlim(0, 100) # Zoom in on the relevant low frequencies
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    \"\"\"
