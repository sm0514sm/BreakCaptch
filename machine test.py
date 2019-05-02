# test, train 폴더가 필요하며
# 홀수 이미지 파일은 A, 짝수 이미지 파일은 F를 나타내야한다.

from sklearn import linear_model
from sklearn import svm
from PIL import Image
import os
import matplotlib.pyplot as plt
import cv2


X_train = []
Y_train = []

X_test = []
Y_test = []


def Xinput(name):
    im = Image.open(name)
    px = im.load()
    inp = []
    for y in range(im.height):
        for x in range(im.width):
            inp.append(px[x, y][0])
    return inp


train_file_list = os.listdir("./train")
train_file_list.sort()
for file_name in train_file_list:
    X_train.append(Xinput("./train/" + file_name))
Y_train = [1, 0] * (len(train_file_list)//2)

test_file_list = os.listdir("./test")
test_file_list.sort()
for file_name in test_file_list:
    X_test.append(Xinput("./test/" + file_name))
Y_test = [1, 0] * (len(test_file_list)//2)

logreg = linear_model.LogisticRegression()
logreg.fit(X_train, Y_train)
y_test_estimated = logreg.predict(X_test)
print("A = 1, F = 0")
print("         정답 : [", end="")

for i, y in enumerate(Y_test):
    if i == len(Y_test)-1:
        print(y, end="")
    else:
        print(y, end=" ")
print("]\n")
print("Logistic 결과 :", y_test_estimated)

count = 0
for i, num in enumerate(Y_test):
    if num == y_test_estimated[i]:
        count += 1
print("정확도 : %.2f%%\n" % (count/len(Y_test)*100))


clf = svm.SVC(gamma='scale')
clf.fit(X_train, Y_train)
print("SVM      결과 :", clf.predict(X_test))

count = 0
for i, num in enumerate(Y_test):
    if num == y_test_estimated[i]:
        count += 1
print("정확도 : %.2f%%\n" % (count/len(Y_test)*100))

X = []
Y = []
XX = []
YY = []
num = 1
for i, a in enumerate(X_train):
    if i % 2 == 0:
        Y.append(sum(a))
        X.append(num)
        num += 1
    else:
        YY.append(sum(a))
        XX.append(num)
        num += 1
plt.plot(X, Y, "ro")
plt.plot(XX, YY, "bo")
# plt.show()
