import numpy as np
import soundfile as sf
from stl import mesh
import math
import matplotlib.pyplot as plt
from scipy.fft import rfft,rfftfreq


#parameters:
definefreq = 233
height = 250
radius = 9
layerheight = 0.1
perrevolution = 3
depth = 12

plot = "none"
plotlow = 0
plothigh = 150


data, samplerate = sf.read('/Users/carlosborne/Downloads/soundvase/ensamble.wav')
#fundamental + fundamental * 3/2 (true 5th) + fundamental * 2^(7/12) (tuned instrument 5th)

y = rfft(data/data.max()*32767)
xf = rfftfreq(data.size, 1/samplerate)
if plot == "freqs":
    plt.plot(xf[np.absolute(xf-plotlow).argmin():np.absolute(xf-plothigh).argmin()],np.abs(y)[np.absolute(xf-plotlow).argmin():np.absolute(xf-plothigh).argmin()])
if definefreq == "auto":
    largest = 0
    largestfreq = 0
    for i in range(np.abs(y)[:10000].size):
        if np.abs(y)[i] > largest:
            largest = np.abs(y)[i]
            largestfreq = xf[i]
else:
    largestfreq=definefreq

resolution = samplerate/largestfreq
angles = np.arange(0,height*2*math.pi,2*math.pi/resolution/perrevolution)
sine= np.sin(angles)
cosine = np.cos(angles)
level = 0

increment = samplerate/largestfreq/resolution
waveincrement = samplerate/largestfreq
texture = np.zeros(math.floor(height*perrevolution*resolution))
appendi = 0
for layer in range(height): #layer is integer layer of height
    #print("0."+str(layer))
    startindex = math.floor(layer*waveincrement)
    for section in range(perrevolution):
        for i in range(math.floor(resolution)):
            texture[appendi] = np.average(data[startindex+math.floor(i*increment):startindex+math.floor(i*increment+increment)])
            appendi = appendi + 1
texture = texture*depth

bigresolution = resolution*perrevolution

vertices = np.zeros((math.floor(height*bigresolution)+2,3))
appendi = 0
for r in range(height):
    #print("1."+str(r))
    for c in range(math.floor(bigresolution)):
        vertices[appendi] = [sine[c]*(radius+texture[r*math.floor(bigresolution)+c]),cosine[c]*(radius+texture[r*math.floor(bigresolution)+c]),r*layerheight]
        appendi += 1
vertices[appendi] = [0,0,0]
appendi += 1
vertices[appendi] = [0,0,height*layerheight-1]

faces = np.zeros(((height-1)*((math.floor(bigresolution)-1)*2+2)+(math.floor(bigresolution)-1)*2+2,3), dtype=int)
appendi = 0
for r in range(height-1):
    #print("2."+str(r))
    for c in range(math.floor(bigresolution)-1):
        faces[appendi] = [r*math.floor(bigresolution)+c,r*math.floor(bigresolution)+c+1,(r+1)*math.floor(bigresolution)+c]
        appendi += 1
        faces[appendi] = [r*math.floor(bigresolution)+c+1,(r+1)*math.floor(bigresolution)+c,(r+1)*math.floor(bigresolution)+c+1]
        appendi += 1
    faces[appendi] = [(r+1)*math.floor(bigresolution)-1,r*math.floor(bigresolution),(r+2)*math.floor(bigresolution)-1]
    appendi += 1
    faces[appendi] = [r*math.floor(bigresolution),(r+2)*math.floor(bigresolution)-1,(r+1)*math.floor(bigresolution)]
    appendi += 1
for c in range(math.floor(bigresolution)-1):
    faces[appendi] = [math.floor(bigresolution)*height,c,c+1]
    appendi += 1
    faces[appendi] = [math.floor(bigresolution)*height+1,(height-1)*math.floor(bigresolution)+c,(height-1)*math.floor(bigresolution)+c+1]
    appendi += 1
faces[appendi] = [math.floor(bigresolution)*height,math.floor(bigresolution)-1,0]
appendi += 1
faces[appendi] = [math.floor(bigresolution)*height+1,height*math.floor(bigresolution)-1,(height-1)*math.floor(bigresolution)]

cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        cube.vectors[i][j] = vertices[f[j],:]

if definefreq == "auto":
    print(largestfreq)

if plot == "texture":
    plt.plot(texture[plotlow:plothigh])
if plot != "none":
    plt.show()

#cube.save('ensemble2.stl')