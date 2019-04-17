# test2 폴더 내에 train, test 폴더로 나뉘며
# 각각의 폴더에는 알파벳 별로 폴더가 다시 나뉘어야한다.
import mglearn as mglearn
from sklearn import linear_model, svm, tree
from sklearn.svm import NuSVC
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.naive_bayes import GaussianNB, MultinomialNB, ComplementNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from PIL import Image
from sklearn import datasets
import matplotlib.pyplot as plt
import os
import numpy
import pandas

X_train = []
Y_train = []
Y_train_num = []

X_test = []
Y_test = []
Y_test_num = []

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
        if folder == "./train":
            X_train.append(XinputRGBPlus("./test2/" + folder + "/" + alphabet + "/" + file_name))
            Y_train.append(alphabet)
            Y_train_num.append(ord(alphabet)-65)
        elif folder == "./test":
            X_test.append(XinputRGBPlus("./test2/" + folder + "/" + alphabet + "/" + file_name))
            Y_test.append(alphabet)
            Y_test_num.append(ord(alphabet) - 65)


def DoImageML():
    for char in alpha:
        path_input("./train", char)
        path_input("./test", char)


# -------------------------------------------------------------------------------------------------- #

def sound_input(csv_file_name, X, Y):
    csv_data = pandas.read_csv('test.csv')
    header = list(csv_data.columns)
    for i in header:
        Y.append(i[2:3])
    row_count = len(csv_data)
    column_count = len(Y)
    csv_array = csv_data.values     # header 값을 제외한 값들
    for j in range(len(Y)):
        temp_X = []
        for i in range(row_count):
            temp_X.append(csv_array[i][j])
        X.append(temp_X)


def DoSoundML():
    sound_input("./train.csv", X_train, Y_train)
    sound_input("./test.csv", X_test, Y_test)


# ----------------------------------------------------------------- #
# DoImageML()
DoSoundML()     # 두개 동시에 실행하면 안됨

print("정답 : [", end="")
for i, y in enumerate(Y_test):
    if i == len(Y_test)-1:
        print("\'%s\'" % y, end="")
    else:
        print("\'%s\'" % y, end=" ")
print("]")

# ----------------------------------------------------------------- #

logreg = linear_model.LogisticRegression()
logreg.fit(X_train, Y_train)
print("Logistic", end=" ")
print("정확도 : %.2f%%" % (logreg.score(X_test, Y_test)*100))
print("결과 :", logreg.predict(X_test))

logreg = linear_model.LogisticRegression(solver='sag', max_iter=100, random_state=42, multi_class='ovr')
logreg.fit(X_train, Y_train)
print("Logistic ovr", end=" ")
print("정확도 : %.2f%%" % (logreg.score(X_test, Y_test)*100))
print("결과 :", logreg.predict(X_test))

logreg = linear_model.LogisticRegression(solver='sag', max_iter=100, random_state=42, multi_class='multinomial')
logreg.fit(X_train, Y_train)
print("Logistic multinomial", end=" ")
print("정확도 : %.2f%%" % (logreg.score(X_test, Y_test)*100))
print("결과 :", logreg.predict(X_test))

clf = svm.SVC(gamma='scale', decision_function_shape='ovo', probability=True)
model = clf.fit(X_train, Y_train)
# print(model.predict_proba([Xinput("./test2/test/Z/ACBZB_result_3.png")]))   # 해당 이미지가 어느 알파벳에 속하는지 확률
print("SVM(SVC)     ", end=" ")
print("정확도 : %.2f%%" % (clf.score(X_test, Y_test)*100))
print("결과 :", clf.predict(X_test))

lin_clf = svm.LinearSVC()
lin_clf.fit(X_train, Y_train)
print("SVM(LinearSVC)     ", end=" ")
print("정확도 : %.2f%%" % (lin_clf.score(X_test, Y_test)*100))
print("결과 :", lin_clf.predict(X_test))

clf = NuSVC(gamma='scale', nu=0.1)
clf.fit(X_train, Y_train)
print("SVM(NuSVC)     ", end=" ")
print("정확도 : %.2f%%" % (clf.score(X_test, Y_test)*100))


clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train, Y_train)
print("tree(DecisionTreeClassifier)", end=" ")
print("정확도 : %.2f%%" % (clf.score(X_test, Y_test)*100))


clf = KNeighborsClassifier(n_neighbors=3)
clf.fit(X_train, Y_train)
print("Nearest Neighbors(KNeighborsClassifier)", end=" ")
print("정확도 : %.2f%%" % (clf.score(X_test, Y_test)*100))


clf = NearestCentroid()
clf.fit(X_train, Y_train)
print("Nearest Neighbors(NearestCentroid)", end=" ")
print("정확도 : %.2f%%" % (clf.score(X_test, Y_test)*100))


clf = GaussianNB()
clf.fit(X_train, Y_train)
print("Naive Bayes(GaussianNB)", end=" ")
print("정확도 : %.2f%%" % (clf.score(X_test, Y_test) * 100))


try:
    clf = MultinomialNB()
    clf.fit(X_train, Y_train)
    print("Naive Bayes(MultinomialNB)", end=" ")
    print("정확도 : %.2f%%" % (clf.score(X_test, Y_test) * 100))
except:
    print("Naive Bayes(MultinomialNB) 측정 불가")


try:
    clf = ComplementNB()
    clf.fit(X_train, Y_train)
    print("Naive Bayes(ComplementNB)", end=" ")
    print("정확도 : %.2f%%" % (clf.score(X_test, Y_test) * 100))
except:
    print("Naive Bayes(ComplementNB) 측정 불가")


try:
    clf = SGDClassifier(loss="hinge", penalty="l2", max_iter=5)
    clf.fit(X_train, Y_train)
    print("SGDClassifier", end=" ")
    print("정확도 : %.2f%%" % (clf.score(X_test, Y_test)*100))
except:
    print("SGDClassifier 측정 불가")

try:
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(X_train, Y_train)
    print("Ensemble methods(RandomForestClassifier)", end=" ")
    print("정확도 : %.2f%%" % (clf.score(X_test, Y_test)*100))
except:
    print("Ensemble methods(RandomForestClassifier)")

try:
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    clf.fit(X_train, Y_train)
    print("Neural network models(MLPClassifier)", end=" ")
    print("정확도 : %.2f%%" % (clf.score(X_test, Y_test)*100))
except:
    print("Neural network models(MLPClassifier)", end=" ")
# neighbors_settings = range(1, 11)
# training_accuracy = []
# test_accuracy = []
#
# for n_neighbors in neighbors_settings:
#     # 모델 생성
#     clf = KNeighborsClassifier(n_neighbors=n_neighbors)
#     clf.fit(X_train, Y_train)
#     # 훈련 세트 정확도 저장
#     training_accuracy.append(clf.score(X_train, Y_train))
#     # 일반화 정확도 저장
#     test_accuracy.append(clf.score(X_test, Y_test))
#
# plt.plot(neighbors_settings, training_accuracy, label="Train Accuracy")
# plt.plot(neighbors_settings, test_accuracy, label="Test Accuracy")
# plt.ylabel("Accuracy")
# plt.xlabel("n_neighbors")
# plt.legend()
# plt.show()
