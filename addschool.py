from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3

conn = sqlite3.connect('data.sqlite')
curr = conn.cursor()


class AddSchool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add School')
        self.setWindowIcon(QIcon('icon/online-course.png'))
        self.setGeometry(450, 100, 350, 550)

        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        self.titleText = QLabel("Add School")
        self.titleText.setFont(QFont("SansSerif", 20))
        self.titleText.setAlignment(Qt.AlignCenter)

        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("School Name")
        self.websiteEntry = QLineEdit()
        self.websiteEntry.setPlaceholderText('School Website')
        self.savebtn = QPushButton('Save')
        self.savebtn.clicked.connect(self.AddSchool)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.bottomLayout.addRow(QLabel("Website: "), self.websiteEntry)
        self.bottomLayout.addRow(QLabel(''),self.savebtn)

        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def AddSchool(self):
        name = self.nameEntry.text()
        website = self.websiteEntry.text()
        if name and website:
            try:
                query1 = f""" SELECT ID FROM School WHERE LOWER(School.Name) == '{name.lower()}'"""
                curr.execute(query1)
                schoolid = curr.fetchall()
                if schoolid == []:
                    query = """ INSERT INTO School (Name,Website,CourseCount)  VALUES(?,?,?)"""
                    curr.execute(query, (name,website,0))
                    conn.commit()
                    QMessageBox.information(self, 'Info', 'School Has Been added successfully')
                else:
                    QMessageBox.information(self, 'Info', 'The School is already added')
            except Exception as e:
                QMessageBox.information(self, 'Info', 'School Has not been added successfully')
        else:
            QMessageBox.information(self, 'Info', 'Fields cannot be empty')
