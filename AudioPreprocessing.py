from pydub import AudioSegment #음성 편집
import wave
import os  # 디렉터리 생성
import numpy as np
from scipy.io.wavfile import read
from DoMachineLearning import SoundMachine


MAX_SIZE = 7000
NULL_SIZE = 3450

class Audio_Preprocessing:
    def cut_by_null(self, hey_audio):
        anp = np.array(hey_audio[1], dtype=int)
        # 음성 파일 가져오기 <- 원래는 웹페이지에서 가져와야함.

        cnt = -1
        i = 0
        null_count = np.empty(0)
        alpha = np.empty(0)
        answer = np.empty(MAX_SIZE)

        # 0 자르기
        while i < anp.size:
            if anp[i] == 0:
                while i < anp.size and anp[i] == 0:
                    null_count = np.append(null_count, anp[i])
                    i += 1
                if null_count.size < 10:
                    alpha = np.append(alpha, null_count)  # 중간의 0
                else:  # 빈공간 0
                    alpha = self.pad_null(without_null=alpha)
                    if cnt in range(0, 4): answer = self.add_on_answer(alpha=alpha, answer=answer)
                    alpha = np.empty(0)
                    cnt += 1
                null_count = np.empty(0)
            else:
                alpha = np.append(alpha, anp[i])
                i += 1
        # print(audio[cnt], cnt, alpha.size, null_count.size, i, anp.size)
        alpha = self.pad_null(without_null=alpha)
        answer = self.add_on_answer(alpha=alpha, answer=answer)
        answer = answer[1:, :]
        # np.savetxt('./' + 'asdfasdf' + '.csv', answer, header='Z', fmt='%d')
        self.delete_listen_wav()
        return answer

    def add_on_answer(self, alpha, answer):
        new = np.vstack([answer, alpha])
        return new

    def pad_null(self, without_null):
        pad = np.zeros(MAX_SIZE - without_null.size)
        with_null = np.append(without_null, pad)
        return with_null

    def delete_listen_wav(self):
        file = './listen.wav' # TODO: 파일명 달라서 삭제 안됨 수정바람 (지마켓이랑 위메프 오디오 파일명 다름)
        if os.path.isfile(file):
            os.remove(file)
        else:
            print('file doesn\'t exist')

def OneSoundProcessingAndML():
    pre = Audio_Preprocessing()
    audio = pre.cut_by_null(hey_audio=read('./' + "captcha" + '.wav'))
    audio = audio.T
    result = SoundMachine.DoMLOneSound("SoundModel.pkl", audio)
    return result[0] + result[1] + result[2] + result[3] + result[4]


if __name__ == '__main__':
    pre2 = Audio_Preprocessing()
    audio = pre2.cut_by_null(hey_audio=read('./' + "captcha" + '.wav'))
    audio = audio.T
    print(SoundMachine.DoMLOneSound("SoundModel.pkl", audio))

