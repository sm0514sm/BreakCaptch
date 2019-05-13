# 이미지는 train_test_image 폴더 내에 train, test 폴더로 나뉘며
# 각각의 폴더에는 알파벳 별로 폴더가 다시 나뉘어야한다.
# 음성은 동일한 폴더 내에 train.csv, test.csv 파일이 존재해야한다.
from sklearn import linear_model
from sklearn.externals import joblib
from PIL import Image
import os
import pandas
import time

alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"    # 해당 문자열에 포함된 문자만 학습 후 테스트 함


def XinputWithName(name):
    im = Image.open(name)
    px = im.load()
    inp = []
    for y in range(im.height):
        for x in range(im.width):
            inp.append(px[x, y][0])
    return inp


def XinputRGBPlusWithName(name):
    im = Image.open(name)
    px = im.load()
    inp = []
    for y in range(im.height):
        for x in range(im.width):
            inp.append(px[x, y][0] + px[x, y][1] + px[x, y][2])
    return inp


def XinputRGBPlusWithImage(image):
    px = image.load()
    inp = []
    for y in range(image.height):
        for x in range(image.width):
            inp.append(px[x, y][0] + px[x, y][1] + px[x, y][2])
    return inp


# -------------------------------------------------------------------------------------------------- #
class LearnedMachine:
    def __init__(self):
        self.X_train = []
        self.Y_train = []
        self.X_test = []
        self.Y_test = []

    def DoModelSave(self, save_model_name):
        logreg = linear_model.LogisticRegression(solver='lbfgs', multi_class='auto')
        logreg.fit(self.X_train, self.Y_train)
        joblib.dump(logreg, "./" + save_model_name + ".pkl")
        print("model saved.")


class ImageMachine(LearnedMachine):
    def image_train_input(self):
        for char in alpha:
            train_file_list = os.listdir("./train_test_image/train/" + char + "/")
            train_file_list.sort()
            for file_name in train_file_list:
                self.X_train.append(XinputRGBPlusWithName("./train_test_image/train/" + char + "/" + file_name))
                self.Y_train.append(char)

    def image_test_input(self):
        for char in alpha:
            test_file_list = os.listdir("./train_test_image/test/" + char + "/")
            test_file_list.sort()
            for file_name in test_file_list:
                self.X_test.append(XinputRGBPlusWithName("./train_test_image/test/" + char + "/" + file_name))
                self.Y_test.append(char)

    def DoMachineLearning(self, model_name):
        logreg = joblib.load(model_name)
        print("Logistic", end=" ")
        print("정확도 : %.2f%%" % (logreg.score(self.X_test, self.Y_test) * 100))
        print("결과 :", logreg.predict(self.X_test))

    # 문자 1개에 대한 ML을 진행해 결과를 return
    @staticmethod
    def DoMLOneImage(model_name, target_image):
        test = []
        test.append(XinputRGBPlusWithImage(target_image))
        logreg = joblib.load(model_name)
        return logreg.predict(test)


class SoundMachine(LearnedMachine):
    def sound_train_input(self, csv_file_name):
        csv_data = pandas.read_csv(csv_file_name)
        header = list(csv_data.columns)
        for i in header:
            self.Y_train.append(i[2:3])
        row_count = len(csv_data)
        column_count = len(self.Y_train)
        csv_array = csv_data.values     # header 값을 제외한 값들
        for j in range(column_count):
            temp_X = []
            for i in range(row_count):
                temp_X.append(csv_array[i][j])
            self.X_train.append(temp_X)

    def sound_test_input(self, csv_file_name):
        csv_data = pandas.read_csv(csv_file_name)
        header = list(csv_data.columns)
        for i in header:
            self.Y_test.append(i[2:3])
        row_count = len(csv_data)
        column_count = len(self.Y_test)
        csv_array = csv_data.values     # header 값을 제외한 값들
        for j in range(column_count):
            temp_X = []
            for i in range(row_count):
                temp_X.append(csv_array[i][j])
            self.X_test.append(temp_X)

    def DoML_Test(self, model_name):
        logreg = joblib.load(model_name)
        return logreg.predict(self.X_test)

    # 음성 1개에 대한 ML을 진행해 결과를 return
    @staticmethod
    def DoMLOneSound(model_name, csv_data):
        row_count = len(csv_data)
        csv_array = csv_data
        test = []
        for j in range(5):
            temp = []
            for i in range(row_count):
                temp.append(csv_array[i][j])
            test.append(temp)

        logreg = joblib.load(model_name)
        return logreg.predict(test)


# ----------------------------------------------------------------- #
if __name__ == "__main__":
    start_time = time.time()
    try:
        SML = SoundMachine()

        # print("모델학습")
        # SML.sound_train_input("./train.csv")
        # SML.DoModelSave("SoundModel")

        print("모델테스트")
        SML.sound_test_input("./test.csv")
        print(SML.DoML_Test("SoundModel.pkl"))
    except BaseException as e:
        print("Sound ML Exception : ", e)
    print("WorkingTime: %.2f sec" % (time.time() - start_time))

    start_time = time.time()
    try:
        IML = ImageMachine()

        # print("모델학습")
        # IML.image_train_input()
        # IML.DoModelSave("ImageModel")

        print("모델테스트")
        IML.image_test_input()
        IML.DoMachineLearning("ImageModel.pkl")
    except BaseException as e:
        print("Image ML Exception : ", e)
    print("WorkingTime: %.2f sec" % (time.time() - start_time))


