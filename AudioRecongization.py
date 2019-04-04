from pydub import AudioSegment #음성 편집
import os #디렉터리 생성

audio = "ZUGEP"

#음성 파일 가져오기
sound = AudioSegment.from_wav("audio/" + audio + ".wav")
print(sound.duration_seconds)

#음성 짜른 구간지정
duration = sound.duration_seconds/5*1000
print(duration)

#알파벳 별로 자르기
first_alphabet = sound[:duration]
second_alphabet = sound[duration:duration*2]
third_alphabet = sound[duration*2:duration*3]
fourth_alphabet = sound[duration*3:duration*4]
fifth_alphabet = sound[-duration:]

#폴더 생성
dir = audio + "/"
if not os.path.isdir(dir):
    os.mkdir(dir)
    #음성 파일 생성
    first_alphabet.export(dir + "1.wav", format="wav")
    second_alphabet.export(dir + "2.wav", format="wav")
    third_alphabet.export(dir + "3.wav", format="wav")
    fourth_alphabet.export(dir + "4.wav", format="wav")
    fifth_alphabet.export(dir + "5.wav", format="wav")

print(first_alphabet.duration_seconds)

# import librosa
# import librosa.display
# import IPython.display
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# import matplotlib.font_manager as fm
#
# y, sr = librosa.load('CKPJR.wav')
# IPython.display.Audio(data=y, rate=sr)
#
# D = librosa.amplitude_to_db(np.abs(librosa.stft(y[:1024])), ref=np.max)
#
# plt.plot(D.flatten())
# plt.show()
#
# S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)
#
# log_S = librosa.logamplitude(S, ref_power=np.max)
# plt.figure(figsize=(12,4))
# librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='mel')
# plt.title('mel power spectrogram')
# plt.colorbar(format='%+02.0f dB')
# plt.tight_layout()
# plt.show()