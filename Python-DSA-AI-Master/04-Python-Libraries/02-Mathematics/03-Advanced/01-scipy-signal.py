"""
Module: scipy.signal - Advanced Signal Processing in Python

Description:
This module serves as a textbook-grade interactive lesson on `scipy.signal`,
a powerful subpackage within SciPy dedicated to signal processing. Signal 
processing is ubiquitous in fields ranging from audio and image processing
to finance, telecommunications, and biomedical engineering.

Learning Objectives:
1. Understand the fundamental mathematical concepts behind signal processing:
   - Convolution and Cross-Correlation
   - Filtering (FIR and IIR filters)
   - Spectral Analysis (Fourier Transforms, Spectrograms, Welch's method)
   - LTI (Linear Time-Invariant) System analysis
2. Implement these concepts using `scipy.signal`.
3. Analyze the time and space complexity (Big-O) of these operations.
4. Solve practical, real-world problems such as noise removal and frequency extraction.

-------------------------------------------------------------------------------
Mathematical Background:
-------------------------------------------------------------------------------

1. Convolution:
For two discrete 1D signals f and g, the convolution (f * g)[n] is defined as:
    (f * g)[n] = sum_{m=-infty}^{infty} f[m] * g[n - m]
Complexity: Naive implementation is O(N*M), where N and M are the lengths of 
the signals. `scipy.signal.fftconvolve` uses the Fast Fourier Transform (FFT) 
to reduce this to O((N+M) log(N+M)).

2. Cross-Correlation:
Similar to convolution, but without time-reversing the second signal:
    (f * g)[n] = sum_{m=-infty}^{infty} f^*[m] * g[n + m]
Used extensively for template matching and finding time delays.

3. Filtering (LTI Systems):
A digital filter can be described by a difference equation:
    a[0]*y[n] + a[1]*y[n-1] + ... + a[k]*y[n-k] = b[0]*x[n] + b[1]*x[n-1] + ... + b[m]*x[n-m]
Where:
    - x[n] is the input signal.
    - y[n] is the output signal.
    - b are the feedforward (numerator) coefficients (FIR part).
    - a are the feedback (denominator) coefficients (IIR part).
Filters modify the frequency content of a signal (e.g., Low-pass, High-pass, Band-pass).

-------------------------------------------------------------------------------
"""

import time
import math
from typing import Tuple, List, Optional, Union, Dict

import numpy as np
import scipy.signal as signal
from scipy.fft import fft, fftfreq


def generate_noisy_signal(duration: float = 1.0, fs: float = 1000.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generates a synthetic composite signal containing two sine waves with added Gaussian noise.
    
    Args:
        duration (float): Length of the signal in seconds. Default is 1.0.
        fs (float): Sampling frequency in Hz. Default is 1000.0.
        
    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray]: 
            - t: Time array.
            - clean_signal: The signal without noise.
            - noisy_signal: The signal with Gaussian noise.
            
    Time Complexity: O(N) where N is the number of samples.
    Space Complexity: O(N) to store the arrays.
    """
    print("--- Generating Synthetic Signal ---")
    
    # N is the total number of samples
    N = int(duration * fs)
    
    # Create time vector from 0 to duration
    t = np.linspace(0, duration, N, endpoint=False)
    
    # Fundamental frequencies
    freq1, freq2 = 50.0, 120.0  # 50 Hz and 120 Hz
    
    # Create clean signal as a sum of two sine waves
    # Formula: A * sin(2 * pi * f * t)
    clean_signal = 1.5 * np.sin(2 * np.pi * freq1 * t) + 2.0 * np.sin(2 * np.pi * freq2 * t)
    
    # Generate Gaussian white noise
    # np.random.normal(mean, std_dev, size)
    noise_power = 0.5
    noise = np.random.normal(0, np.sqrt(noise_power), N)
    
    noisy_signal = clean_signal + noise
    
    print(f"Generated signal of length {N} samples (Duration: {duration}s, Fs: {fs}Hz)")
    print(f"Signal components: {freq1}Hz and {freq2}Hz sine waves.")
    print("-----------------------------------\n")
    
    return t, clean_signal, noisy_signal


def demonstrate_filtering(t: np.ndarray, noisy_signal: np.ndarray, fs: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Demonstrates designing and applying a digital Low-Pass Filter using scipy.signal.
    
    We aim to filter out the 120Hz frequency and the high-frequency noise, 
    leaving only the 50Hz component.
    
    Args:
        t (np.ndarray): Time array.
        noisy_signal (np.ndarray): The input noisy signal.
        fs (float): Sampling frequency.
        
    Returns:
        Tuple[np.ndarray, np.ndarray]:
            - filtered_signal_fir: Output from the FIR filter.
            - filtered_signal_iir: Output from the IIR (Butterworth) filter.
            
    Time Complexity:
        - IIR Filtering (lfilter/filtfilt): O(N * max(len(a), len(b)))
        - FIR Filtering (fftconvolve): O(N log N)
    Space Complexity: O(N) to store output signals.
    """
    print("--- Digital Filtering (FIR vs IIR) ---")
    
    nyquist = 0.5 * fs
    cutoff_freq = 80.0  # We want to keep 50 Hz, but block 120 Hz and above
    
    # Normalizing the cutoff frequency to Nyquist (required for standard filter design functions)
    normalized_cutoff = cutoff_freq / nyquist
    
    # ==========================================
    # 1. IIR Filter Design (Butterworth)
    # ==========================================
    # Butterworth filters have a maximally flat frequency response in the passband.
    # Order 4 is chosen as a trade-off between roll-off steepness and stability/delay.
    order = 4
    
    # `b` (numerator) and `a` (denominator) coefficients of the IIR filter
    b_iir, a_iir = signal.butter(order, normalized_cutoff, btype='low', analog=False)
    
    # Applying the filter using `filtfilt`
    # filtfilt applies the filter forward and then backward. This results in zero phase shift,
    # meaning the filtered signal aligns perfectly in time with the input signal.
    # If we used `lfilter`, there would be a time delay (phase shift).
    filtered_iir = signal.filtfilt(b_iir, a_iir, noisy_signal)
    
    print(f"Designed order-{order} IIR Butterworth low-pass filter (Cutoff: {cutoff_freq}Hz).")
    
    # ==========================================
    # 2. FIR Filter Design (Window Method)
    # ==========================================
    # FIR filters are always unconditionally stable and can be designed to have exact linear phase.
    numtaps = 101 # Must be odd for certain filter types. Higher number = steeper roll-off but more computation.
    
    # Design using firwin
    # We use a Hamming window by default to reduce Gibbs phenomenon (ringing).
    b_fir = signal.firwin(numtaps, normalized_cutoff, window='hamming')
    a_fir = [1.0] # FIR filters have no feedback loop, so the denominator is just 1.
    
    # Apply using filtfilt (zero-phase)
    filtered_fir = signal.filtfilt(b_fir, a_fir, noisy_signal)
    
    print(f"Designed {numtaps}-tap FIR low-pass filter (Cutoff: {cutoff_freq}Hz).")
    
    # Calculate Mean Squared Error (MSE) to compare (assuming we want to isolate the 50Hz signal)
    ideal_50hz = 1.5 * np.sin(2 * np.pi * 50.0 * t)
    
    mse_iir = np.mean((filtered_iir - ideal_50hz) ** 2)
    mse_fir = np.mean((filtered_fir - ideal_50hz) ** 2)
    
    print(f"MSE (IIR) relative to pure 50Hz: {mse_iir:.4f}")
    print(f"MSE (FIR) relative to pure 50Hz: {mse_fir:.4f}")
    print("--------------------------------------\n")
    
    return filtered_fir, filtered_iir


def demonstrate_spectral_analysis(noisy_signal: np.ndarray, fs: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Demonstrates estimating the Power Spectral Density (PSD) using Welch's method.
    
    Welch's method splits the signal into overlapping segments, computes the periodogram 
    for each, and averages them. This reduces the variance of the PSD estimate compared 
    to a raw FFT periodogram, at the cost of frequency resolution.
    
    Args:
        noisy_signal (np.ndarray): The input signal.
        fs (float): Sampling frequency.
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: Frequencies and corresponding PSD values.
        
    Time Complexity: O(K * M log M) where K is number of segments and M is segment length.
    Space Complexity: O(M) for the segment processing.
    """
    print("--- Spectral Analysis (Welch's Method) ---")
    
    # Using a Hann window with 256 samples per segment and 50% overlap
    nperseg = 256
    overlap = nperseg // 2
    
    frequencies, psd = signal.welch(
        noisy_signal, 
        fs, 
        nperseg=nperseg, 
        noverlap=overlap,
        scaling='density'
    )
    
    # Find the dominant frequencies (peaks in the PSD)
    # We use find_peaks from scipy.signal
    peaks, properties = signal.find_peaks(psd, height=np.max(psd)*0.1)
    
    print("Identified dominant frequencies from PSD:")
    for peak_idx in peaks:
        freq = frequencies[peak_idx]
        power = psd[peak_idx]
        print(f"  -> Frequency: {freq:.2f} Hz, Power: {power:.4f}")
        
    print("Notice how Welch's method clearly identifies the 50Hz and 120Hz components despite the noise.")
    print("------------------------------------------\n")
    
    return frequencies, psd


def demonstrate_convolution_correlation() -> None:
    """
    Demonstrates 1D convolution and cross-correlation, their differences,
    and performance considerations (Direct vs FFT-based).
    
    Time Complexity:
        Direct: O(N * M)
        FFT-based: O((N+M) log(N+M))
    """
    print("--- Convolution and Cross-Correlation ---")
    
    # 1. Simple convolution example
    sig = np.array([0, 1, 2, 3, 2, 1, 0])
    kernel = np.array([1, 1, 1]) / 3.0  # A simple moving average filter
    
    # mode='same' returns output of the same length as sig, centered.
    conv_result = signal.convolve(sig, kernel, mode='same')
    print(f"Original Signal: {sig}")
    print(f"Kernel (Moving Avg): {kernel}")
    print(f"Convolved (Smoothed): {np.round(conv_result, 2)}")
    
    # 2. Cross-correlation (Template matching)
    # Finding a specific pattern in a noisy signal
    pattern = np.array([1, -1, 1, -1])
    # Create a sequence with the pattern embedded
    sequence = np.random.randn(20) * 0.1
    sequence[8:12] += pattern  # Embed at index 8
    
    # mode='valid' returns only those parts of the cross-correlation that are computed 
    # without zero-padding.
    correlation_result = signal.correlate(sequence, pattern, mode='valid')
    best_match_idx = np.argmax(correlation_result)
    
    print(f"\nPattern embedded at index: 8")
    print(f"Cross-correlation found best match at index: {best_match_idx}")
    
    # 3. Performance benchmark: Direct vs FFT Convolution
    print("\nBenchmarking Convolution (Direct vs FFT) for large arrays...")
    large_sig = np.random.randn(100_000)
    large_kernel = np.random.randn(5_000)
    
    # Scipy 1.4+ `convolve` automatically chooses the fastest method (direct vs fft)
    # if `method='auto'`, but we will force them to show the difference.
    
    start = time.perf_counter()
    signal.convolve(large_sig, large_kernel, method='direct')
    time_direct = time.perf_counter() - start
    
    start = time.perf_counter()
    signal.convolve(large_sig, large_kernel, method='fft')
    time_fft = time.perf_counter() - start
    
    print(f"  Direct O(N*M) Time: {time_direct:.4f} seconds")
    print(f"  FFT O(N log N) Time: {time_fft:.4f} seconds")
    print(f"  Speedup: {time_direct / time_fft:.2f}x")
    print("-----------------------------------------\n")


def interview_challenge(signal_array: np.ndarray, window_size: int) -> np.ndarray:
    """
    Common Interview/Practical Challenge:
    Implement a moving average filter (boxcar filter) over a 1D array.
    Instead of using loops (which are slow in Python), use scipy.signal/numpy 
    vectorized operations to achieve O(N) or O(N log N) time complexity.
    
    Args:
        signal_array (np.ndarray): The input 1D data array.
        window_size (int): The size of the moving window.
        
    Returns:
        np.ndarray: The smoothed array.
    """
    print("--- Interview Challenge: Moving Average Filter ---")
    if window_size < 1:
        raise ValueError("Window size must be at least 1")
    if window_size > len(signal_array):
        raise ValueError("Window size cannot be larger than the signal")
        
    # Create the filter kernel. A moving average is essentially convolution 
    # with an array of 1/W, where W is the window size.
    kernel = np.ones(window_size) / window_size
    
    # Perform convolution. Using 'valid' means the output length is len(signal_array) - window_size + 1
    # We'll use 'same' to keep the length identical, padding with zeros at the edges implicitly.
    smoothed = signal.convolve(signal_array, kernel, mode='same', method='auto')
    
    print(f"Input array size: {len(signal_array)}, Window size: {window_size}")
    print("Moving average computed efficiently via convolution.")
    print("--------------------------------------------------\n")
    return smoothed


def solve_lti_system() -> None:
    """
    Demonstrates working with Linear Time-Invariant (LTI) Systems.
    Simulates the step response and impulse response of a continuous-time system.
    
    Consider a simple mass-spring-damper system (2nd order ODE):
    m*x''(t) + c*x'(t) + k*x(t) = f(t)
    
    Transfer function H(s) = X(s)/F(s) = 1 / (m*s^2 + c*s + k)
    """
    print("--- LTI Systems: Transfer Functions and Responses ---")
    
    m = 1.0   # Mass (kg)
    c = 0.5   # Damping coefficient (N.s/m) - Underdamped system
    k = 2.0   # Spring constant (N/m)
    
    # Numerator and Denominator of the Transfer Function
    num = [1.0]
    den = [m, c, k]
    
    # Define the LTI system
    system = signal.TransferFunction(num, den)
    print(f"Defined LTI System Transfer Function:\n{system}")
    
    # Compute Step Response
    # step() returns time array and system response
    t_step, y_step = signal.step(system)
    
    # Compute Impulse Response
    t_impulse, y_impulse = signal.impulse(system)
    
    # Look at some characteristics
    peak_time = t_step[np.argmax(y_step)]
    peak_value = np.max(y_step)
    steady_state = y_step[-1] # Approximation
    overshoot = ((peak_value - steady_state) / steady_state) * 100 if steady_state != 0 else 0
    
    print(f"System Characteristics (Step Response):")
    print(f"  -> Peak Time: {peak_time:.2f} s")
    print(f"  -> Peak Value: {peak_value:.3f}")
    print(f"  -> Steady State (Approx): {steady_state:.3f}")
    print(f"  -> Overshoot: {overshoot:.1f}%")
    print("-----------------------------------------------------\n")


def run_tests() -> None:
    """
    Test suite to validate correctness of the implementations and edge cases.
    """
    print("--- Running Comprehensive Tests ---")
    
    # Test 1: Moving Average Challenge
    test_arr = np.array([1, 2, 3, 4, 5])
    window = 3
    # Expected with mode='same':
    # padded: [0, 1, 2, 3, 4, 5, 0]
    # conv: [(0+1+2)/3, (1+2+3)/3, (2+3+4)/3, (3+4+5)/3, (4+5+0)/3]
    # conv: [1.0, 2.0, 3.0, 4.0, 3.0]
    res = interview_challenge(test_arr, window)
    expected = np.array([1.0, 2.0, 3.0, 4.0, 3.0])
    assert np.allclose(res, expected), f"Test 1 Failed: {res} != {expected}"
    print("[PASS] Moving Average Convolution Logic")
    
    # Test 2: Edge Case for Moving Average - Window size 1 (identity)
    res = interview_challenge(test_arr, 1)
    assert np.allclose(res, test_arr), "Test 2 Failed"
    print("[PASS] Moving Average Edge Case (Window=1)")
    
    # Test 3: Correlation exact match
    sig = np.array([0, 1, 0, 0])
    pat = np.array([1])
    res = signal.correlate(sig, pat, mode='valid')
    assert np.allclose(res, sig), "Test 3 Failed"
    print("[PASS] Cross-correlation Identity match")
    
    print("All tests passed successfully!\n")


if __name__ == "__main__":
    print("=" * 60)
    print("  SCIPY.SIGNAL: MASTERING DIGITAL SIGNAL PROCESSING")
    print("=" * 60 + "\n")
    
    # Configuration
    FS = 1000.0 # Hz
    DURATION = 2.0 # Seconds
    
    # 1. Generation
    t_arr, clean_arr, noisy_arr = generate_noisy_signal(duration=DURATION, fs=FS)
    
    # 2. Filtering
    fir_filtered, iir_filtered = demonstrate_filtering(t_arr, noisy_arr, FS)
    
    # 3. Spectral Analysis
    freqs, psd = demonstrate_spectral_analysis(noisy_arr, FS)
    
    # 4. Convolution & Correlation
    demonstrate_convolution_correlation()
    
    # 5. LTI Systems
    solve_lti_system()
    
    # 6. Tests & Interview Challenge
    run_tests()
    
    print("=" * 60)
    print("  END OF SCIPY.SIGNAL LESSON")
    print("=" * 60)
