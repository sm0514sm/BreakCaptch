from pydub import AudioSegment #음성 편집
import wave
import os #디렉터리 생성
import sys
import numpy as np
from scipy.io.wavfile import read

MAX_SIZE = 11000
NULL_SIZE = 3451

def audio_cut():
    # 함수로 만들어서 다른 파일들이랑 이어붙여야함
    # 그러려면 음성파일을 웹페이지에서 가져와서 넣는거 해줘야함.

    audio = "WFFNW"

    #음성 파일 가져오기 <- 원래는 웹페이지에서 가져와야함.
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

    print(first_alphabet)

def padding_audio():
    audio = "1 (2)"

    # 음성 파일 가져오기 <- 원래는 웹페이지에서 가져와야함.

    a = read('train/Z/' + audio + '.wav')
    anp = np.array(a[1], dtype=int)
    print(anp)
    print(anp.size)
    pad = np.zeros(11000-anp.size)
    first = np.append(anp, pad)
    print(first.size)
    np.savetxt('./' + audio + '.csv', first.T, header='Z', fmt='%d')  # 횡으로 저장하는방법 모르게쑴

def cut_by_null():
    audio = "ABFDO"
    # 음성 파일 가져오기 <- 원래는 웹페이지에서 가져와야함.

    a = read('audio/' + audio + '.wav')
    anp = np.array(a[1], dtype=int)
    print(anp.size)
    cnt = 0
    i = NULL_SIZE
    alpha = np.arange(0)
    # 0 자르기
    while i < anp.size:
        if anp[i] == 0 and anp[i + 1] == 0:
            i += 3451
            pad = np.zeros(MAX_SIZE - alpha.size)
            alpha = np.append(alpha, pad)
            np.savetxt("./" + audio[cnt] + ".csv", alpha.T, header=audio[cnt], fmt='%d')
            alpha = np.arange(0)
            cnt += 1
        else:
            print('[', i, ']    ', anp[i])
            alpha = np.append(alpha,anp[i])
            # first = np.array(anp[i:i+ 11000], dtype=int)
            i += 1


if __name__ == '__main__':
    # audio_cut()
    cut_by_null()

#폴더 생성
# dir = audio + "/"
# if not os.path.isdir(dir):
#     os.mkdir(dir)
#     음성 파일 생성
    # first_alphabet.export(dir + "1.wav", format="wav")
    # second_alphabet.export(dir + "2.wav", format="wav")
    # third_alphabet.export(dir + "3.wav", format="wav")
    # fourth_alphabet.export(dir + "4.wav", format="wav")
    # fifth_alphabet.export(dir + "5.wav", format="wav")
#
# print(first_alphabet.duration_seconds)

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