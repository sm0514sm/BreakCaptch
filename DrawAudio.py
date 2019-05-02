import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
from scipy.io.wavfile import read

spf = wave.open('audio/WFFNW.wav','r')
a = read('audio/ABFDO.wav')
anp = np.array(a[1], dtype=int)


# csv로 저장
np.savetxt("./sample.csv", anp.T, fmt='%d') #횡으로 저장하는방법 모르게쑴

#Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')

#print(signal)
#f = open('wave.txt','w')
# signal.tofile(f)
#f.close()

#If Stereo
# if spf.getnchannels() == 2:
#     print('Just mono files')
#     sys.exit(0)
#
plt.figure(1)
plt.title('Signal Wave...')
plt.plot(signal)
plt.show()