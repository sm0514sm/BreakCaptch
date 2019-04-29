# 이미지는 test2 폴더 내에 train, test 폴더로 나뉘며
# 각각의 폴더에는 알파벳 별로 폴더가 다시 나뉘어야한다.
# 음성은 동일한 폴더 내에 train.csv, test.csv 파일이 존재해야한다.
import mglearn as mglearn
from sklearn import linear_model
from sklearn.externals import joblib
from PIL import Image
import os
import pandas
import time

alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"    # 해당 문자열에 포함된 문자만 학습 후 테스트 함

def Xinput(name):
    im = Image.open(name)
    px = im.load()
    inp = []
    for y in range(im.height):
        for x in range(im.width):
            inp.append(px[x, y][0])
    return inp


def XinputRGBPlus(name):
    im = Image.open(name)
    px = im.load()
    inp = []
    for y in range(im.height):
        for x in range(im.width):
            inp.append(px[x, y][0] + px[x, y][1] + px[x, y][2])
    return inp


def path_input(folder, alphabet):
    global Y_train
    train_file_list = os.listdir("./test2/" + folder + "/" + alphabet + "/")
    train_file_list.sort()
    for file_name in train_file_list:
        if folder == "train":
            X_train.append(XinputRGBPlus("./test2/" + folder + "/" + alphabet + "/" + file_name))
            Y_train.append(alphabet)
        elif folder == "test":
            X_test.append(XinputRGBPlus("./test2/" + folder + "/" + alphabet + "/" + file_name))
            Y_test.append(alphabet)


# -------------------------------------------------------------------------------------------------- #

def sound_input(csv_file_name, X, Y):
    csv_data = pandas.read_csv(csv_file_name)
    header = list(csv_data.columns)
    for i in header:
        Y.append(i[2:3])
    row_count = len(csv_data)
    column_count = len(Y)
    csv_array = csv_data.values     # header 값을 제외한 값들
    for j in range(column_count):
        temp_X = []
        for i in range(row_count):
            temp_X.append(csv_array[i][j])
        X.append(temp_X)


# ----------------------------------------------------------------- #

def DoModelSave(save_model_name):
    logreg = linear_model.LogisticRegression(solver='lbfgs', multi_class='auto')
    logreg.fit(X_train, Y_train)
    joblib.dump(logreg, "./" + save_model_name + ".pkl")
    print("model saved.")


def DoMachineLearning(model_name):
    logreg = joblib.load(model_name)

    print("Logistic", end=" ")
    print("정확도 : %.2f%%" % (logreg.score(X_test, Y_test)*100))
    print("결과 :", logreg.predict(X_test))

# ----------------------------------------------------------------- #


if __name__ == "__main__":
    X_train = []
    Y_train = []
    X_test = []
    Y_test = []
    start_time = time.time()
    # sound_input("./train.csv", X_train, Y_train)
    # DoModelSave("SoundModel")
    sound_input("./test.csv", X_test, Y_test)
    DoMachineLearning("SoundModel.pkl")
    print("WorkingTime: %.2f sec" % (time.time() - start_time))
    print()

    X_train.clear()
    Y_train.clear()
    X_test.clear()
    Y_test.clear()
    start_time = time.time()
    # for char in alpha:
    #     path_input("train", char)
    # SetImageTrainTest()
    # DoModelSave("ImageModel")
    for char in alpha:
        path_input("test", char)
    DoMachineLearning("ImageModel.pkl")
    print("WorkingTime: %.2f sec" % (time.time() - start_time))


