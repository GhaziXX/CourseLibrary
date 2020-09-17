import sqlite3

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import addschool
from ExtendedComboBox import ExtendedComboBox

conn = sqlite3.connect('data.sqlite')
curr = conn.cursor()


class AddInstructor(QWidget):
    def __init__(self, obj, school=None, ins=None):
        super().__init__()
        self.setWindowTitle('Add Instructor')
        self.setWindowIcon(QIcon('icon/online-learning.png'))
        self.setGeometry(450, 100, 350, 550)
        self.obj = obj
        self.school = school
        self.ins = ins
        self.setFixedSize(self.size())
        self.UI()
        if self.school is None and self.ins is None:
            self.show()
        else:
            self.AddInstructor()

    def UI(self):
        self.get_Defaults()
        self.widgets()
        self.layouts()

    def widgets(self):
        self.titleText = QLabel("Add Instructor")
        self.titleText.setFont(QFont("SansSerif", 20))
        self.titleText.setAlignment(Qt.AlignCenter)

        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Instructor Name")
        self.schoolEntry = ExtendedComboBox()
        self.addSchool = QPushButton('Add')
        self.addSchool.clicked.connect(self.add_School)
        self.savebtn = QPushButton('Save')
        self.savebtn.clicked.connect(self.AddInstructor)

        self.schoolEntry.addItems(sorted(self.schools))

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
        self.addSchoolLayout = QHBoxLayout()

        self.addSchoolLayout.addWidget(self.schoolEntry)
        self.addSchoolLayout.addWidget(self.addSchool)

        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.bottomLayout.addRow(QLabel("School: "), self.addSchoolLayout)
        self.bottomLayout.addRow(QLabel(''), self.savebtn)

        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def add_School(self):
        self.AddSchool = addschool.AddSchool(self.obj)

    def AddInstructor(self):
        if self.ins is not None and self.school is not None:
            name = self.ins
            school = self.school
        else:
            name = self.nameEntry.text().replace("'", "''")
            school = self.schoolEntry.currentText().replace("'", "''")
        if name and school:
            try:
                query1 = f""" SELECT ID FROM Instructor WHERE LOWER(Instructor.Name) == '{name.lower()}'"""
                curr.execute(query1)
                instructorid = curr.fetchall()
                query2 = f""" SELECT ID FROM School WHERE LOWER(School.Name) == '{school.lower()}'"""
                curr.execute(query2)
                schoolid = curr.fetchall()
                if instructorid == []:
                    if schoolid == []:
                        QMessageBox.information(self, "School Doesn't Exist",
                                                'Please Add the school to the database before using it')
                    else:
                        query = """INSERT INTO Instructor (Name,CoursesCount,SchoolID)  VALUES(?,?,?)"""
                        curr.execute(query, (name, 0, schoolid[0][0]))
                        if instructorid != []:
                            count_query = f''' SELECT count(*) FROM Course WHERE InstructorID='{instructorid[0][0]}' '''
                            count = curr.execute(count_query)
                            count = count[0][0] if count != [] else 0
                            update_query = f''' UPDATE Instructor SET CoursesCount={count} WHERE InstructorID = {instructorid[0][0]}'''
                            curr.execute(update_query)
                        conn.commit()
                        QMessageBox.information(self, 'Info', 'Instructor Has Been added succesfully')
                        self.obj.funcRefresh()
                        self.close()
                else:
                    QMessageBox.information(self, 'Info', 'The Instructor is already added')
                    self.close()
            except Exception as e:
                QMessageBox.information(self, 'Info', 'Instructor Has not been added succesfully')
        else:
            QMessageBox.information(self, 'Info', 'Fields cannot be empty!')

    def get_Defaults(self):
        s = curr.execute('SELECT DISTINCT Name FROM School')
        self.schools = [i[0] for i in s]
