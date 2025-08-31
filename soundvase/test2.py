import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np

"""
data, samplerate = sf.read('/Users/carlosborne/Downloads/soundvase/soundvase1.wav')
plt.plot(data[0:8000])
print(samplerate)
plt.show()
"""

faces = np.zeros((8,3))
faces[3] = [1,2,3]
print(faces)