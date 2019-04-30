from pydub import AudioSegment #음성 편집
import wave
import os #디렉터리 생성
import sys
import numpy as np
from scipy.io.wavfile import read

MAX_SIZE = 7000
NULL_SIZE = 3450

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
    pad = np.zeros(MAX_SIZE-anp.size)
    first = np.append(anp, pad)
    print(first.size)
    np.savetxt('./' + audio + '.csv', first.T, header='Z', fmt='%d')  # 횡으로 저장하는방법 모르게쑴

def cut_by_null():
    audio = "NJWJA"
    # 음성 파일 가져오기 <- 원래는 웹페이지에서 가져와야함.

    a = read('audio/' + audio + '.wav')
    anp = np.array(a[1], dtype=int)
    print(anp.size)
    np.savetxt("./" + audio + ".csv", anp.T, fmt='%d')
    cnt = -1
    null_count = np.arange(0)
    i = 0
    alpha = np.arange(0)
    # 0 자르기
    while i < anp.size:
        if anp[i] == 0:
            while i < anp.size and anp[i] == 0:
                null_count = np.append(null_count, anp[i])
                i += 1
            if null_count.size < 10 : alpha = np.append(alpha, null_count) #중간의 0
            else : #빈공간 0
                pad = np.zeros(MAX_SIZE - alpha.size)
                alpha = np.append(alpha, pad)
                if cnt in range(0,4): np.savetxt("./" + audio[cnt] + ".csv", alpha.T, header=audio[cnt], fmt='%d')
                print(audio[cnt], cnt, alpha.size, null_count.size, i, anp.size)
                alpha = np.arange(0)
                cnt += 1
            null_count = np.arange(0)
        else:
           # print('[', i, ']    ', anp[i])
            alpha = np.append(alpha,anp[i])
            # first = np.array(anp[i:i+ 11000], dtype=int)
            i += 1
    print(audio[cnt], cnt, alpha.size, null_count.size, i, anp.size)
    np.savetxt("./" + audio[cnt] + ".csv", alpha.T, header=audio[cnt], fmt='%d')


if __name__ == '__main__':
    # audio_cut()
    cut_by_null()