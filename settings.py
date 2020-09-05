from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Settings(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Settings')
        self.setWindowIcon(QIcon('icon/settings.png'))
        self.setGeometry(450, 100, 350, 550)

        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def get_vals(self):
        with open('settings.txt', 'r') as f:
            r = f.readlines()
            down = True if r[0][:-1] == 'True' else False
            uplo = True if r[-1] == 'True' else False
        return down, uplo

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        self.titleText = QLabel("Settings")
        self.titleText.setFont(QFont("SansSerif", 20))
        self.titleText.setAlignment(Qt.AlignCenter)

        d, u = self.get_vals()
        self.download = QCheckBox()
        self.download.setChecked(d)
        self.download.setText("Download Database On each Opening")
        self.upload = QCheckBox()
        self.upload.setChecked(u)
        self.upload.setText("Upload Database Automatically when quitting")
        self.savebtn = QPushButton('Save')
        self.savebtn.clicked.connect(self.Save)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow(QLabel(""), self.download)
        self.bottomLayout.addRow(QLabel(""), self.upload)
        self.bottomLayout.addRow(QLabel(''), self.savebtn)

        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def Save(self):
        with open('settings.txt', 'w') as f:
            f.writelines([str(self.download.isChecked()), '\n', str(self.upload.isChecked())])
        self.close()
