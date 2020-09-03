import sqlite3

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import addinstructor
import addschool
from ExtendedComboBox import ExtendedComboBox

conn = sqlite3.connect('data.sqlite')
curr = conn.cursor()


class AddCourse(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Course')
        self.setWindowIcon(QIcon('icon/courses.png'))
        self.setGeometry(450, 100, 350, 550)

        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.get_Defaults()
        self.widgets()
        self.layouts()

    def widgets(self):
        self.titleText = QLabel("Add Course")
        self.titleText.setFont(QFont("SansSerif", 20))
        self.titleText.setAlignment(Qt.AlignCenter)

        self.titleEntry = QLineEdit()
        self.titleEntry.setPlaceholderText("Course Title")
        self.categoryEntry = ExtendedComboBox()
        self.tagsEntry = QLineEdit()
        self.tagsEntry.setPlaceholderText("Tags comma separated")
        self.durationEntry = QLineEdit()
        self.durationEntry.setPlaceholderText("Duration")
        self.linkEntry = QLineEdit()
        self.linkEntry.setPlaceholderText('Link')
        self.directoryEntry = ExtendedComboBox()
        self.stateEntry = ExtendedComboBox()
        self.instructorEntry = ExtendedComboBox()
        self.addInstructor = QPushButton('Add')
        self.addInstructor.clicked.connect(self.add_Instructor)
        self.schoolEntry = ExtendedComboBox()
        self.addSchool = QPushButton('Add')
        self.addSchool.clicked.connect(self.add_School)
        self.savebtn = QPushButton('Save')
        self.savebtn.clicked.connect(self.addCourse)

        self.schoolEntry.addItems(sorted(self.schools))
        self.instructorEntry.addItems(sorted(self.instructors))
        self.categoryEntry.addItems(sorted(self.categories))
        self.directoryEntry.addItems(['2', '1', '3'])
        self.stateEntry.addItems(['Not Completed', 'Completed'])

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
        self.addInstructorLayout = QHBoxLayout()
        self.addSchoolLayout = QHBoxLayout()

        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)

        self.addInstructorLayout.addWidget(self.instructorEntry)
        self.addInstructorLayout.addWidget(self.addInstructor)
        self.addSchoolLayout.addWidget(self.schoolEntry)
        self.addSchoolLayout.addWidget(self.addSchool)

        self.bottomLayout.addRow(QLabel("Title: "), self.titleEntry)
        self.bottomLayout.addRow(QLabel("School: "), self.addSchoolLayout)
        self.bottomLayout.addRow(QLabel("Instructor: "), self.addInstructorLayout)
        self.bottomLayout.addRow(QLabel("Category: "), self.categoryEntry)
        self.bottomLayout.addRow(QLabel("Tags: "), self.tagsEntry)
        self.bottomLayout.addRow(QLabel("Duration: "), self.durationEntry)
        self.bottomLayout.addRow(QLabel("Link: "), self.linkEntry)
        self.bottomLayout.addRow(QLabel("Directory: "), self.directoryEntry)
        self.bottomLayout.addRow(QLabel("State: "), self.stateEntry)
        self.bottomLayout.addRow(QLabel(''), self.savebtn)

        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def addCourse(self):
        title = self.titleEntry.text().replace("'", "''")
        category = self.categoryEntry.currentText().replace("'", "''")
        tags = self.tagsEntry.text().replace("'", "''")
        duration = self.durationEntry.text().replace("'", "''")
        link = self.linkEntry.text().replace("'", "''")
        directory = self.directoryEntry.currentText().replace("'", "''")
        state = self.stateEntry.currentText().replace("'", "''")
        instructor = self.instructorEntry.currentText().replace("'", "''")
        school = self.schoolEntry.currentText().replace("'", "''")
        if title and category and tags and duration and link and directory and state and instructor and school:
            try:
                query1 = f""" SELECT ID FROM School WHERE LOWER(School.Name) == '{school.lower()}'"""
                curr.execute(query1)
                schoolid = curr.fetchall()
                query2 = f""" SELECT ID FROM Instructor WHERE LOWER(Instructor.Name) == '{instructor.lower()}'"""
                curr.execute(query2)
                instructorid = curr.fetchall()
                if schoolid == []:
                    QMessageBox.information(self, "School Doesn't Exist",
                                            'Please Add the school to the database before using it')
                elif instructorid == []:
                    QMessageBox.information(self, "Instructor Doesn't Exist",
                                            'Please Add the instructor to the database before using it')
                elif schoolid == [] and instructorid == []:
                    QMessageBox.information(self, "Instructor and School Doesn't Exist",
                                            'Please Add the instructor and the school to the database before using it')
                else:
                    query = """ INSERT INTO Course (Title,Category,Duration,Link,IsCompleted,Directory,Tags,SchoolID,InstructorID) VALUES(?,?,?,?,?,?,?,?,?)"""
                    curr.execute(query, (
                        title, category, duration, link, state, directory, tags, schoolid[0][0], instructorid[0][0]))
                    count_query = f''' SELECT count(*) FROM Course WHERE SchoolID='{schoolid[0][0]}' '''
                    curr.execute(count_query)
                    count = curr.fetchall()[0][0]
                    update_query = f''' UPDATE School SET CourseCount={count} WHERE ID = {schoolid[0][0]}'''
                    curr.execute(update_query)
                    count_query = f''' SELECT count(*) FROM Course WHERE InstructorID='{instructorid[0][0]}' '''
                    curr.execute(count_query)
                    count = curr.fetchall()[0][0]
                    update_query = f''' UPDATE Instructor SET CoursesCount={count} WHERE ID = {instructorid[0][0]}'''
                    curr.execute(update_query)
                    conn.commit()
                    QMessageBox.information(self, 'Info', 'Course Has Been added succesfully')
                    self.close()
            except Exception as e:
                QMessageBox.information(self, 'Info', 'Course has not been added')
        else:
            QMessageBox.information(self, 'Info', 'Fields cannot be empty')

    def add_School(self):
        self.add_school = addschool.AddSchool()

    def add_Instructor(self):
        self.add_intructor = addinstructor.AddInstructor()

    def get_Defaults(self):
        s = curr.execute('SELECT DISTINCT Name FROM School')
        self.schools = [i[0] for i in s]
        i = curr.execute('SELECT DISTINCT Name FROM Instructor')
        self.instructors = [j[0] for j in i]
        c = curr.execute('SELECT DISTINCT Category FROM Course')
        self.categories = [i[0] for i in c]
