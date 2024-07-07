import time
import numpy as np
import sounddevice as sd

def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave

def beep(frequency=440, duration=0.1, sample_rate=44100):
    wave = generate_sine_wave(frequency, duration, sample_rate)
    sd.play(wave, sample_rate)
    sd.wait()

def sleep(duration):
    for _ in range(duration):
        time.sleep(1)
        beep()
