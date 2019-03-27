import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import OpenChromeCrawling


# 개인정보입력 창
class LogInDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.id = None
        self.password = None
        self.phone = None

    def setupUI(self):
        self.setGeometry(1100, 200, 300, 100)
        self.setWindowTitle("개인정보 입력")
        # self.setWindowIcon(QIcon('icon.png'))

        # 라벨링
        label1 = QLabel("이름: ")
        label2 = QLabel("생년월일: ")
        label3 = QLabel("휴대폰번호: ")

        
        self.lineEdit1 = QLineEdit()
        self.lineEdit2 = QLineEdit()
        self.lineEdit3 = QLineEdit()
        # 콤보박스 - 내국인외국인
        cb = QComboBox(self)
        cb.addItems(["내국인", "외국인"])
        cb.currentTextChanged.connect(self.onActivated)
        self.setWindowTitle('QComboBox')
        # 라디오버튼 - 남여
        self.rbtn1 = QRadioButton('남', self)
        self.rbtn2 = QRadioButton('여', self)
        # 확인 버튼
        self.pushButton1= QPushButton("확인")
        self.pushButton1.clicked.connect(self.pushButtonClicked)

        layout = QGridLayout()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.lineEdit1, 0, 1)
        # 콤보박스
        layout.addWidget(cb, 0, 2)
        layout.addWidget(label2, 1, 0)
        layout.addWidget(self.lineEdit2, 1, 1)
        layout.addWidget(self.rbtn1, 1, 2)
        layout.addWidget(self.rbtn2, 1, 3)
        layout.addWidget(label3, 2, 0)
        layout.addWidget(self.lineEdit3, 2, 1)
        layout.addWidget(self.pushButton1, 3, 0)
        self.setLayout(layout)

    def onActivated(self, text):
        # TODO 선택된 옵션 메인창의 label로 넘기기 <-수정
        #self.nation = cb.text()
        #self.lbl.adjustSize()
        print('combooooo')

    def pushButtonClicked(self):
        self.id = self.lineEdit1.text()
        self.password = self.lineEdit2.text()
        self.phone = self.lineEdit3.text()
        OpenChromeCrawling.set_user_info(self.id, 0, self.password, self.phone, 0, 0, 0)
        self.close()


# 메인창
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)
        self.setWindowTitle("R U Robot")
        # self.setWindowIcon(QIcon('icon.png'))

        self.pushButton1 = QPushButton("개인정보 입력")
        self.pushButton1.clicked.connect(self.openPersonalInformation)
        self.pushButton2 = QPushButton("크롬 열기")
        self.pushButton2.clicked.connect(self.openCrome)
        self.label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.pushButton1)
        layout.addWidget(self.pushButton2)
        layout.addWidget(self.label)

        self.setLayout(layout)

    # 개인정보 입력 창 띄우기
    def openPersonalInformation(self):
        dlg = LogInDialog()
        dlg.exec_()
        id = dlg.id
        password = dlg.password
        phone = dlg.phone
        self.label.setText("id: %s password: %s phone: %s nationality : " % (id, password, phone))

    # 크롬 열기
    def openCrome(self):
        OpenChromeCrawling.do_crawling()
        # TODO do_crawling()이 돌아가는 동안 GUI 가 완전히 먹통됨 >> do_crawling 을 subprocess 로 작동 필요
        print('열려라 디버깅크롬크롬')
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
