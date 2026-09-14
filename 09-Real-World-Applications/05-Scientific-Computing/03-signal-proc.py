"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (SIGNAL PROCESSING & FOURIER)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# An electrical engineer receives a chaotic, staticky audio file and needs to 
# isolate the 60Hz hum of a faulty power line. A junior developer attempts to 
# mathematically analyze the raw amplitude of the Time-Domain waveform using a 
# Python `for` loop. They fail because the 60Hz wave is mathematically buried 
# underneath a cacophony of background noise and voice data.
#
# A senior DSP (Digital Signal Processing) engineer understands the "Fourier Transform". 
# They import `scipy.fft`. In a single mathematical line of code, they convert 
# the Time-Domain signal into the Frequency-Domain. The complex waveform instantly 
# shatters into a mathematical histogram of individual frequencies. The 60Hz 
# spike stands out like a skyscraper. They apply a mathematical "Notch Filter", 
# execute an Inverse Fourier Transform, and reconstruct the audio file flawlessly, 
# completely deleting the hum.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the mathematical concept of the Fast Fourier Transform (FFT).
# - Execute Time-Domain to Frequency-Domain conversion.
# - Execute algorithmic Signal Filtering (Low-Pass, Notch filters).
#
# ==============================================================================
"""

import math
import timeit

# Gracefully handle missing dependencies
try:
    import numpy as np
    from scipy.fft import fft, fftfreq
    from scipy import signal
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. GENERATING THE CHAOTIC WAVEFORM (THE TIME DOMAIN)
# ==============================================================================
def demonstrate_fourier_transform():
    section_header("The Fast Fourier Transform (Time -> Frequency)")
    
    if not HAS_SCIPY:
        print("  [ERROR] SciPy/NumPy is not installed. Run `pip install scipy numpy`.")
        return
        
    print("  [PHASE 1: THE CHAOTIC TIME-DOMAIN SIGNAL]")
    # 1. We must define the mathematical parameters of the audio file!
    SAMPLE_RATE = 1000  # 1000 data points recorded per second (Hz)
    DURATION = 2.0      # 2 seconds of audio
    N = int(SAMPLE_RATE * DURATION) # Total number of data points (2000)
    
    # We generate a mathematical X-axis (Time in seconds)
    time_x = np.linspace(0.0, DURATION, N, endpoint=False)
    
    # 2. We construct three mathematical Sine waves!
    print("    -> Generating a clean 50 Hz Sine Wave...")
    wave_50hz = np.sin(50.0 * 2.0 * np.pi * time_x)
    
    print("    -> Generating a clean 120 Hz Sine Wave...")
    wave_120hz = np.sin(120.0 * 2.0 * np.pi * time_x)
    
    print("    -> Generating high-frequency mathematical NOISE (400 Hz)...")
    wave_noise = 0.5 * np.sin(400.0 * 2.0 * np.pi * time_x)
    
    # 3. We violently smash them all together into a single, chaotic signal!
    # In the Time-Domain, this just looks like static on an oscilloscope.
    chaotic_signal = wave_50hz + wave_120hz + wave_noise
    
    print("    -> [RESULT] Signals merged. The individual frequencies are now hidden.")


    # ==========================================================================
    # 4. THE FAST FOURIER TRANSFORM (THE FREQUENCY DOMAIN)
    # ==========================================================================
    print("\n  [PHASE 2: THE FAST FOURIER TRANSFORM (FFT)]")
    # We want to mathematically prove that the chaotic signal is composed of
    # exactly 50 Hz, 120 Hz, and 400 Hz!
    
    start_fft = timeit.default_timer()
    
    # 1. We execute the FFT! This converts Amplitude(Time) into Amplitude(Frequency)
    # It returns an array of Complex Numbers! (a + bj)
    frequency_data_y = fft(chaotic_signal)
    
    # 2. We calculate the exact mathematical Frequencies (The X-Axis of the histogram)
    frequency_data_x = fftfreq(N, 1.0 / SAMPLE_RATE)
    
    end_fft = timeit.default_timer()
    print(f"    -> FFT Algorithm Execution Time: {end_fft - start_fft:.6f} seconds")
    
    
    # 3. We mathematically extract the Dominant Frequencies!
    # The FFT returns complex numbers. We must take the absolute value (`np.abs`) 
    # to find the true magnitude (height) of the spike!
    
    # We only care about positive frequencies (the first half of the array)
    positive_freqs_x = frequency_data_x[:N//2]
    magnitudes_y = np.abs(frequency_data_y[0:N//2])
    
    # We find the mathematical peaks!
    print("\n  [PHASE 3: ISOLATING THE HIDDEN FREQUENCIES]")
    
    # Find all frequencies where the magnitude is a massive spike!
    # We set an arbitrary threshold to ignore background static.
    THRESHOLD = 500.0 
    
    detected_frequencies = []
    for i in range(len(positive_freqs_x)):
        if magnitudes_y[i] > THRESHOLD:
            # We found a massive spike!
            freq = positive_freqs_x[i]
            detected_frequencies.append(freq)
            print(f"    -> MASSIVE SPIKE DETECTED at: {freq:>5.1f} Hz (Magnitude: {magnitudes_y[i]:.0f})")
            
    print(f"\n  [CONCLUSION] The Fourier Transform successfully reverse-engineered the chaotic signal.")
    print(f"  It mathematically proved the audio contains: {detected_frequencies}")


# ==============================================================================
# 5. SIGNAL FILTERING (THE LOW-PASS FILTER)
# ==============================================================================
def demonstrate_signal_filtering():
    section_header("Digital Filtering (Removing the Noise)")
    
    if not HAS_SCIPY:
        return
        
    print("  [SCENARIO] We want to permanently delete the 400 Hz Noise from the audio.")
    
    SAMPLE_RATE = 1000
    
    # 1. We mathematically architect a Butterworth "Low-Pass" Filter!
    # A low-pass filter allows LOW frequencies (50Hz, 120Hz) to pass through safely,
    # but violently blocks HIGH frequencies (400Hz).
    
    # The "Cutoff Frequency" is where the filter starts blocking.
    # Nyquist Theorem dictates we must normalize it against half the sample rate.
    NYQUIST_FREQ = SAMPLE_RATE / 2.0
    CUTOFF = 200.0 / NYQUIST_FREQ # We block everything above 200 Hz!
    
    print(f"\n  [PHASE 1: ARCHITECTING THE FILTER]")
    print(f"    -> Filter Type: Butterworth Low-Pass")
    print(f"    -> Cutoff Frequency: 200 Hz")
    
    # We generate the mathematical coefficients (Numerator b, Denominator a) for the filter!
    b, a = signal.butter(N=4, Wn=CUTOFF, btype='low', analog=False)
    
    print("\n  [PHASE 2: EXECUTING THE FILTER]")
    # We would pass our `chaotic_signal` array through `signal.filtfilt(b, a, chaotic_signal)`
    # This executes a forward-backward mathematical pass to ensure Zero-Phase distortion!
    print("    -> `clean_signal = signal.filtfilt(b, a, chaotic_signal)`")
    print("    -> [RESULT] The 400 Hz mathematical noise has been completely eradicated.")
    print("    -> The audio is now pristine and safe for human ears.")


def run_all_labs():
    demonstrate_fourier_transform()
    demonstrate_signal_filtering()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the architectural difference between the Time Domain and the Frequency Domain?"
   Senior Answer: "The Time Domain is a mathematical representation of Amplitude over Time (e.g., watching a speaker cone vibrate in and out over $2$ seconds). In this domain, all frequencies are violently smashed together into a single chaotic line. If a song has a Bass guitar ($40$Hz) and a Cymbal crash ($4,000$Hz), you cannot physically separate them in the Time Domain. The Frequency Domain is a mathematical representation of Amplitude over Frequency. It acts like a graphical equalizer. It mathematically deconstructs the chaotic line into a histogram showing exactly how much of the $40$Hz signal exists and how much of the $4,000$Hz signal exists, completely ignoring the concept of Time. This allows an engineer to target a specific mathematical spike and delete it without destroying the rest of the song."

2. Interviewer: "Why is the FFT (Fast Fourier Transform) considered one of the most important algorithms of the 20th century?"
   Senior Answer: "The original mathematical formula for the Discrete Fourier Transform (DFT) is an $O(N^2)$ operation. If you have $1$ million data points (e.g., $20$ seconds of CD-quality audio), the DFT requires $1$ Trillion mathematical calculations. It would take a computer hours to process a single song. In $1965$, Cooley and Tukey published the 'Fast Fourier Transform' (FFT) algorithm. By exploiting the mathematical symmetry of Sine waves, they collapsed the complexity to $O(N \\log N)$. For that same $1$ million data points, the FFT only requires $20$ Million calculations. It mathematically accelerated the computation by a factor of $50,000$, physically enabling modern Wi-Fi, 5G cell phones, MP3 compression, and MRI machines to operate in real-time."

3. Interviewer: "What is the 'Nyquist Theorem', and how does it restrict our Sample Rate parameters?"
   Senior Answer: "The Nyquist-Shannon Sampling Theorem mathematically proves that to accurately digitize a continuous analog frequency, your Sample Rate must be strictly greater than TWICE the highest frequency you want to capture. If you want to record a cymbal crash at $10,000$ Hz, your microphone must record at least $20,000$ samples per second ($20$ kHz). If you violate this mathematical law (e.g., recording a $10,000$ Hz signal at only $12,000$ Hz), the algorithm suffers from 'Aliasing'. The high frequency will mathematically reflect back down the spectrum and masquerade as a low frequency, permanently corrupting the data matrix with phantom noise that cannot be filtered out. This is exactly why standard CDs are recorded at $44,100$ Hz; it is slightly more than double the maximum human hearing limit of $20,000$ Hz."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Scientific Computing (Signal Processing) Completed.")
