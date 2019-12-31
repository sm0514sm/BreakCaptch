# 실행파일 생성 : pyinstaller --hidden-import sklearn.neighbors.typedefs -w -F --icon=robot.ico GUI.py
# 실행시킬때 GUI.exe 와 같은 폴더에 SoundModel.pkl 이 있어야 함


import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from OpenChromeCrawling import Crawler
import threading
import webbrowser


# TODO 옳지 않은 입력형식 입력시 에러
# TODO Chrome driver 위치 지정
# TODO GUI 이쁘게?
# TODO 


# 개인정보입력 창
class LogInDialog(QDialog):
    def __init__(self):
        super().__init__()
        # self.refresh()
        self.setupUI()
        self.id = None
        self.password = None
        self.phone = None
        self.sex = None
        self.nation = None
        self.agency = None

    def setupUI(self):
        self.setGeometry(1100, 200, 500, 500)
        self.setWindowTitle("개인정보 입력")
        # self.setWindowIcon(QIcon('icon.png'))

        # 라벨링
        label1 = QLabel("이름: ")
        label2 = QLabel("생년월일: ")
        label3 = QLabel("휴대폰번호: ")
        label8 = QLabel("국적")
        label6 = QLabel("통신사")
        label7 = QLabel("성별")
        self.label6 = QLabel('', self)
        self.label6.move(50, 150)

        self.lineEdit1 = QLineEdit()
        self.lineEdit2 = QLineEdit()
        birth = QRegExp("^(19|20)\d{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[0-1])$")
        birth_Validator = QRegExpValidator(birth, self)
        self.lineEdit2.setValidator((birth_Validator))
        self.lineEdit3 = QLineEdit("010")
        hp = QRegExp("010[0-9]{4}[0-9]{4}")
        hp_Validator = QRegExpValidator(hp, self)
        self.lineEdit3.setValidator(hp_Validator)
        # 콤보박스 - 내국인외국인
        self.rbtn1 = QRadioButton('내국인', self)
        self.rbtn2 = QRadioButton('외국인', self)
        self.rbtn3 = QRadioButton('SKT', self)
        self.rbtn4 = QRadioButton('KT', self)
        self.rbtn5 = QRadioButton('LGT', self)
        self.rbtn6 = QRadioButton('알뜰폰', self)
        self.rbtn7 = QRadioButton('남자', self)
        self.rbtn8 = QRadioButton('여자', self)
        self.btg1 = QButtonGroup()
        self.btg1.addButton(self.rbtn1)
        self.btg1.addButton(self.rbtn2)
        self.btg2 = QButtonGroup()
        self.btg2.addButton(self.rbtn7)
        self.btg2.addButton(self.rbtn8)
        # 라디오버튼 - 남여
        # 확인 버튼
        self.pushButton1 = QPushButton("확인")
        self.pushButton1.clicked.connect(self.pushButtonClicked)

        layout = QGridLayout()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.lineEdit1, 0, 1)
        layout.addWidget(label8, 0, 2)
        layout.addWidget(label7, 2, 2)
        layout.addWidget(label6, 5, 0)
        layout.addWidget(self.rbtn7, 3, 2)
        layout.addWidget(self.rbtn8, 3, 4)
        # 콤보박스
        layout.addWidget(label2, 1, 0)
        layout.addWidget(self.lineEdit2, 1, 1)
        layout.addWidget(self.rbtn1, 1, 2)
        layout.addWidget(self.rbtn2, 1, 4)
        layout.addWidget(label3, 2, 0)
        layout.addWidget(self.lineEdit3, 2, 1)
        layout.addWidget(self.rbtn3, 6, 0)
        layout.addWidget(self.rbtn4, 6, 1)
        layout.addWidget(self.rbtn5, 6, 2)
        layout.addWidget(self.rbtn6, 6, 4)
        layout.addWidget(self.pushButton1, 7, 0)
        self.setLayout(layout)

    def refresh(self):
        i = 0
        while i < 10:
            info = open('test.txt', 'r', encoding="utf8")
            line = info.readline()
            if i == 0:
                self.id = line
            if i == 1:
                self.sex = line
            if i == 2:
                self.nation = line
            if i == 3:
                self.agency = line
            if i == 4:
                self.password = line
            if i == 5:
                self.phone = line

        info.close()

    def pushButtonClicked(self):
        self.id = self.lineEdit1.text()
        self.password = self.lineEdit2.text()
        self.phone = self.lineEdit3.text()
        if self.rbtn1.isChecked():
            self.nation = self.rbtn1.text()
        else:
            if self.rbtn2.isChecked():
                self.nation = self.rbtn2.text()
        if self.rbtn3.isChecked():
            self.agency = self.rbtn3.text()
        elif self.rbtn4.isChecked():
            self.agency = self.rbtn4.text()
        elif self.rbtn5.isChecked():
            self.agency = self.rbtn5.text()
        elif self.rbtn6.isChecked():
            self.agency = self.rbtn6.text()
        if self.rbtn7.isChecked():
            self.sex = self.rbtn7.text()
        else:
            if self.rbtn8.isChecked():
                self.sex = self.rbtn8.text()
        # self.nation = self.text1
        # self.agency = self.text2
        crawler.set_user_info(self.id, self.nation, self.password, self.sex, self.agency, self.phone, 0)
        self.close()


# about창
class AboutWindow(QDialog, uic.loadUiType("about.ui")[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        print("일단 들어옴")
        self.linkButton.clicked.connect(self.openGit)
        self.pushButton.clicked.connect(self.close)

    def openGit(self):
        print('opengit')
        webbrowser.open("https://github.com/sm0514sm/BreakCaptcha")


# 메인창
class MyWindow(QWidget, uic.loadUiType("gui.ui")[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.personInfoSetButton.clicked.connect(self.openPersonalInformation)
        self.openChromeButton.clicked.connect(self.openCrome)
        self.chromeSetButton.clicked.connect(self.pushButtonClicked)
        self.aboutButton.clicked.connect(self.openAbout)
        self.exitButton.clicked.connect(self.close)

    def pushButtonClicked(self):
        fname = QFileDialog.getOpenFileName(self)
        print(fname[0])
        print("driver" in fname[0])
        if "driver" not in fname[0]:
            self.chromeLabel.setText("크롬드라이버 : 위치 설정 오류")
            crawler.driver_path = "ERROR"
            print("크롬 드라이버 위치 설정 오류")
        else:
            self.chromeLabel.setText(fname[0])
            crawler.driver_path = self.chromeLabel.text()

    # 개인정보 입력 창 띄우기
    def openPersonalInformation(self):
        dlg = LogInDialog()
        dlg.exec_()
        print("여긴됨")
        id = dlg.id
        sex = dlg.sex
        nation = dlg.nation
        agency = dlg.agency
        password = dlg.password
        phone = dlg.phone
        print("여긴됨")
        self.userLabel.setText("name: %s, nationality : %s, birth: %s, sex : %s, agency : %s, phone: %s"
            % (id, nation, password, sex, agency, phone))

    # 크롬 열기
    def openCrome(self):
        t_crawler = threading.Thread(target=crawler.do_crawling, args=())
        t_crawler.start()

    def openAbout(self):
        print('여기된')
        dlg = AboutWindow()
        dlg.exec_()
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    crawler = Crawler()
    window = MyWindow()
    window.show()
    app.exec_()
