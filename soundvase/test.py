import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import write
from scipy.fft import rfft, rfftfreq

SAMPLE_RATE = 44100  # Hertz
DURATION = 1  # Seconds

def generate_sine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    # 2pi because np.sin takes radians
    y = np.sin((2 * np.pi) * frequencies)
    return x, y


_, nice_tone = generate_sine_wave(300, SAMPLE_RATE, DURATION)
_, noise_tone = generate_sine_wave(2400, SAMPLE_RATE, DURATION)
_, noise_tone2 = generate_sine_wave(8100, SAMPLE_RATE, DURATION)
increasing = np.arange(-1,1,2/SAMPLE_RATE/DURATION)
noise_tone = noise_tone * 0.3 * increasing
noise_tone2 = noise_tone * 0.2 * increasing

mixed_tone = nice_tone + noise_tone + noise_tone2

normalized_tone = np.int16((mixed_tone / mixed_tone.max()) * 32767)

plt.plot(normalized_tone[0:1000])

# Number of samples in normalized_tone
N = SAMPLE_RATE * DURATION

yf = rfft(normalized_tone)
xf = rfftfreq(N, 1 / SAMPLE_RATE)

write("mysinewave.wav", SAMPLE_RATE, normalized_tone)

#plt.plot(xf, np.abs(yf))
plt.show()