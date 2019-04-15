# test2 폴더 내에 train, test 폴더로 나뉘며
# 각각의 폴더에는 알파벳 별로 폴더가 다시 나뉘어야한다.
import mglearn as mglearn
from sklearn import linear_model
from sklearn import svm
from sklearn.svm import NuSVC
from sklearn.linear_model import SGDClassifier
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier, KDTree
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.naive_bayes import GaussianNB, MultinomialNB, ComplementNB, BernoulliNB
from sklearn.cross_decomposition import PLSCanonical, PLSRegression, CCA
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.neural_network import MLPClassifier
from PIL import Image
from sklearn import datasets
import matplotlib.pyplot as plt
import os

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
print("Logistic", end=" ")
print("정확도 : %.2f%%\n" % (logreg.score(X_test, Y_test)*100))


logreg = linear_model.LogisticRegression(solver='sag', max_iter=100, random_state=42, multi_class='ovr')
logreg.fit(X_train, Y_train)
print("Logistic ovr", end=" ")
print("정확도 : %.2f%%\n" % (logreg.score(X_test, Y_test)*100))


logreg = linear_model.LogisticRegression(solver='sag', max_iter=100, random_state=42, multi_class='multinomial')
logreg.fit(X_train, Y_train)
print("Logistic multinomial", end=" ")
print("정확도 : %.2f%%\n" % (logreg.score(X_test, Y_test)*100))


clf = svm.SVC(gamma='scale', decision_function_shape='ovo', probability=True)
model = clf.fit(X_train, Y_train)
# print(model.predict_proba([Xinput("./test2/test/Z/ACBZB_result_3.png")]))   # 해당 이미지가 어느 알파벳에 속하는지 확률
print("SVM(SVC)     ", end=" ")
print("정확도 : %.2f%%\n" % (clf.score(X_test, Y_test)*100))


lin_clf = svm.LinearSVC()
lin_clf.fit(X_train, Y_train)
print("SVM(LinearSVC)     ", end=" ")
print("정확도 : %.2f%%\n" % (lin_clf.score(X_test, Y_test)*100))


clf = NuSVC(gamma='scale', nu=0.1)
clf.fit(X_train, Y_train)
print("SVM(NuSVC)     ", end=" ")
print("정확도 : %.2f%%\n" % (clf.score(X_test, Y_test)*100))


clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train, Y_train)
print("tree(DecisionTreeClassifier)", end=" ")
print("정확도 : %.2f%%\n" % (clf.score(X_test, Y_test)*100))


clf = KNeighborsClassifier(n_neighbors=3)
clf.fit(X_train, Y_train)
print("Nearest Neighbors(KNeighborsClassifier)", end=" ")
print("정확도 : %.2f%%\n" % (clf.score(X_test, Y_test)*100))


clf = NearestCentroid()
clf.fit(X_train, Y_train)
print("Nearest Neighbors(NearestCentroid)", end=" ")
print("정확도 : %.2f%%\n" % (clf.score(X_test, Y_test)*100))


clf = GaussianNB()
clf.fit(X_train, Y_train)
print("Naive Bayes(GaussianNB)", end=" ")
print("정확도 : %.2f%%\n" % (clf.score(X_test, Y_test) * 100))


clf = MultinomialNB()
clf.fit(X_train, Y_train)
print("Naive Bayes(MultinomialNB)", end=" ")
print("정확도 : %.2f%%\n" % (clf.score(X_test, Y_test) * 100))


clf = ComplementNB()
clf.fit(X_train, Y_train)
print("Naive Bayes(ComplementNB)", end=" ")
print("정확도 : %.2f%%\n" % (clf.score(X_test, Y_test) * 100))


clf = SGDClassifier(loss="hinge", penalty="l2", max_iter=5)
clf.fit(X_train, Y_train)
print("SGDClassifier", end=" ")
print("정확도 : %.2f%%\n" % (clf.score(X_test, Y_test)*100))


clf = RandomForestClassifier(n_estimators=10)
clf.fit(X_train, Y_train)
print("Ensemble methods(RandomForestClassifier)", end=" ")
print("정확도 : %.2f%%\n" % (clf.score(X_test, Y_test)*100))


clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
clf.fit(X_train, Y_train)
print("Neural network models(MLPClassifier)", end=" ")
print("정확도 : %.2f%%\n" % (clf.score(X_test, Y_test)*100))
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
