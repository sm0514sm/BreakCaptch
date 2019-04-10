# test2 폴더 내에 train, test 폴더로 나뉘며
# 각각의 폴더에는 알파벳 별로 폴더가 다시 나뉘어야한다.

from sklearn import linear_model
from sklearn import svm
from PIL import Image
import matplotlib.pyplot as plt
import os
import random

X_train = []
Y_train = []

X_test = []
Y_test = []

alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def Xinput(name):
    im = Image.open(name)
    px = im.load()
    inp = []
    for y in range(im.height):
        for x in range(im.width):
            inp.append(px[x, y][0])
    return inp


def path_input(folder, alphabet):
    global Y_train
    train_file_list = os.listdir("./test2/" + folder + "/" + alphabet + "/")
    train_file_list.sort()
    for file_name in train_file_list:
        if folder == "./train":
            X_train.append(Xinput("./test2/" + folder + "/" + alphabet + "/" + file_name))
            Y_train.append(alphabet)
        elif folder == "./test":
            X_test.append(Xinput("./test2/" + folder + "/" + alphabet + "/" + file_name))
            Y_test.append(alphabet)


for char in alpha:
    path_input("./train", char)
    path_input("./test", char)


print("         정답 : [", end="")
for i, y in enumerate(Y_test):
    if i == len(Y_test)-1:
        print("\'%s\'" % y, end="")
    else:
        print("\'%s\'" % y, end=" ")
print("]\n")

# ----------------------------------------------------------------- #

logreg = linear_model.LogisticRegression()
logreg.fit(X_train, Y_train)
y_test_estimated = logreg.predict(X_test)
print("Logistic 결과 :", y_test_estimated)
result = y_test_estimated
count = 0
for i, num in enumerate(Y_test):
    if num == result[i]:
        count += 1
print("정확도 : %.2f%%\n" % (count/len(Y_test)*100))


clf = svm.SVC(gamma='scale', decision_function_shape='ovo')
clf.fit(X_train, Y_train)
result = clf.predict(X_test)
print("SVM      결과 :", clf.predict(X_test))
count = 0
for i, num in enumerate(Y_test):
    if num == result[i]:
        count += 1
print("정확도 : %.2f%%\n" % (count/len(Y_test)*100))
