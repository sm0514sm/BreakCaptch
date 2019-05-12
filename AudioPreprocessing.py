from pydub import AudioSegment #음성 편집
import wave
import os #디렉터리 생성
import sys
import numpy as np
from scipy.io.wavfile import read
import matplotlib.pyplot as plt

MAX_SIZE = 11000

def draw_image():
    spf = wave.open('59313.wav', 'r')

    # Extract Raw Audio from Wav File
    signal = spf.readframes(-1)
    signal = np.fromstring(signal, dtype=np.int16)

    plt.figure(1)
    plt.title('Audio Wave')
    plt.plot(signal)
    plt.show()

def cut_by_null(hey_audio):
    anp = np.array(hey_audio[1], dtype=int)
    # 음성 파일 가져오기 <- 원래는 웹페이지에서 가져와야함.
    audio = "59313"
    cnt = -1
    i = 0
    null_count = np.empty(0)
    alpha = np.empty(0)
    answer = np.empty(MAX_SIZE)

    # 0 자르기
    while i < anp.size:
        if anp[i] == 0 or (anp[i] <= -256 and anp[i] >= -258) :
            while i < anp.size and (anp[i] == 0 or (anp[i] <= -256 and anp[i] >= -258)):
                null_count = np.append(null_count, anp[i])
                i += 1
            if null_count.size < 30 : alpha = np.append(alpha, null_count) #중간의 0
            else : #빈공간 0
                alpha = pad_null(without_null=alpha)
                if cnt in range(0, 4):
                    answer = add_on_answer(alpha=alpha, answer=answer)
                    np.savetxt("./" + audio[cnt] + ".csv", alpha.T, header=audio[cnt], fmt='%d')
                alpha = np.empty(0)
                cnt += 1
            null_count = np.empty(0)
        else:
            alpha = np.append(alpha, anp[i])
            i += 1
    alpha = pad_null(without_null=alpha)
    answer = add_on_answer(alpha=alpha, answer=answer)
    answer = answer[1:,:]
    np.savetxt('./' + alpha[cnt] + '.csv', alpha[cnt], header='Z', fmt='%d')
    delete_listen_wav()
    return answer

def add_on_answer(alpha, answer):
    new = np.vstack([answer, alpha])
    return new

def pad_null(without_null):
    print(without_null.size)
    pad = np.zeros(MAX_SIZE - without_null.size)
    with_null = np.append(without_null, pad)
    return with_null

def delete_listen_wav():
    file = './listen.wav'
    if os.path.isfile(file):
        os.remove(file)
    else: print('file doesn\'t exist')

def temp():
    hey_audio = read('./audio.wav')
    anp = np.array(hey_audio[1], dtype=int)
    np.savetxt('./' + 'heyyyy' + '.csv', anp, fmt='%d')

if __name__ == '__main__':
    draw_image()
    audio = cut_by_null(hey_audio=read("59313" + '.wav'))
    # temp()
