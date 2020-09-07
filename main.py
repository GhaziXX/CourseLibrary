import sqlite3
import sys

import requests
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import addcourse
import addinstructor
import addschool
import cloud
import settings
from ExtendedComboBox import ExtendedComboBox

with open('settings.txt', 'r') as f:
    r = f.readlines()
    down = True if r[0][:-1] == 'True' else False

if down:
    try:
        r = requests.get('http://google.com', timeout=1)
        cloud.download()
    except:
        QMessageBox.information(self, 'Informations', e)

conn = sqlite3.connect('data.sqlite')
curr = conn.cursor()
courseID = 0
schoolID = 0
instructorID = 0
tags = ''
schools, categories, instructors, all_courses, tags = [], [], [], [], []


class Main(QMainWindow):

    def __init__(self):
        global conn
        global curr
        super().__init__()
        self.setWindowTitle("Course Library")
        self.setGeometry(450, 150, 1365, 710)
        self.showMaximized()
        self.UI()
        self.show()

    def UI(self):
        self.toolBar()
        self.widgets()
        self.layouts()
        self.get_Defaults()
        self.filterWidget()
        self.tabWidget()
        self.displayCourses()
        self.displaySchools()
        self.displayInstructors()

    def closeEvent(self, event):
        with open('settings.txt', 'r') as f:
            r = f.readlines()
            uplo = True if r[-1] == 'True' else False
        if uplo:
            try:
                r = requests.get('http://google.com', timeout=1)
                QMessageBox.information(self, 'Updating', 'Please Wait until the database is successfully uploaded')
                cloud.upload()
                event.accept()
            except:
                QMessageBox.information(self, 'Error', 'Please Check your internet access to upload the database')
                event.accept()

    def toolBar(self):
        self.tb = self.addToolBar('Tool Bar')
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addCourse = QAction(QIcon('icon/courses.png'), 'Add Course', self)
        self.tb.addAction(self.addCourse)
        self.addCourse.triggered.connect(self.funcAddCourse)
        self.tb.addSeparator()
        self.addSchool = QAction(QIcon('icon/online-course.png'), 'Add School', self)
        self.tb.addAction(self.addSchool)
        self.addSchool.triggered.connect(self.funcAddSchool)
        self.tb.addSeparator()
        self.addInstructor = QAction(QIcon('icon/online-learning.png'), 'Add Instructor', self)
        self.tb.addAction(self.addInstructor)
        self.addInstructor.triggered.connect(self.funcAddInstructor)
        self.tb.addSeparator()
        self.settings = QAction(QIcon('icon/settings.png'), 'Settings', self)
        self.tb.addAction(self.settings)
        self.settings.triggered.connect(self.funcSettings)
        self.tb.addSeparator()

    def tabWidget(self):
        self.tabs = QTabWidget()
        self.mainLowerLayout.addWidget(self.tabs)
        self.tabs.setLayout(self.mainLowerLayout)
        self.courses = QWidget()
        self.schools = QWidget()
        self.instructors = QWidget()
        self.tabs.addTab(self.courses, 'Courses')
        self.courses.setLayout(self.coursesLayout)
        self.tabs.addTab(self.schools, 'Schools')
        self.schools.setLayout(self.schoolsLayout)
        self.tabs.addTab(self.instructors, 'Instructors')
        self.instructors.setLayout(self.instructorsLayout)

    def filterWidget(self):
        self.schoolCombo = ExtendedComboBox()
        self.schoolCombo.addItem('Schools')
        self.schoolCombo.currentIndexChanged.connect(self.filter)
        self.categoryCombo = ExtendedComboBox()
        self.categoryCombo.addItem('Category')
        self.categoryCombo.currentIndexChanged.connect(self.filter)
        self.directoryCombo = ExtendedComboBox()
        self.directoryCombo.addItems(['Directory', '1', '2', '3', 'Online'])
        self.directoryCombo.currentIndexChanged.connect(self.filter)
        self.iscompletedCombo = ExtendedComboBox()
        self.iscompletedCombo.addItems(['State', 'Completed', 'Not Completed'])
        self.iscompletedCombo.currentIndexChanged.connect(self.filter)
        self.instructorBox = ExtendedComboBox()
        self.instructorBox.addItem('Instructors')
        self.instructorBox.currentIndexChanged.connect(self.filter)
        self.tagsBox = ExtendedComboBox()
        self.tagsBox.addItem('Tags')
        self.tagsBox.currentIndexChanged.connect(self.filter)
        self.searchBox = QLineEdit()
        self.searchBox.setPlaceholderText('Enter Course name')
        self.searchBox.setCompleter(self.get_completer(all_courses, self.searchBox))
        self.searchBox.textEdited.connect(self.searchCourse)
        self.searchBox.returnPressed.connect(self.searchCourse)
        self.searchButton = QPushButton('Search')

        self.mainUpperLayout.addWidget(self.schoolCombo, 20)
        self.mainUpperLayout.addWidget(self.categoryCombo, 20)
        self.mainUpperLayout.addWidget(self.directoryCombo, 20)
        self.mainUpperLayout.addWidget(self.iscompletedCombo, 20)
        self.mainUpperLayout.addWidget(self.instructorBox)
        self.mainUpperLayout.addWidget(self.tagsBox, 20)
        self.mainUpperLayout.addWidget(self.searchBox, 80)
        self.mainUpperLayout.addWidget(self.searchButton)
        self.searchButton.clicked.connect(self.searchCourse)

        self.schoolCombo.addItems(sorted(schools))
        self.categoryCombo.addItems(sorted(categories))
        self.instructorBox.addItems(sorted(instructors))
        self.tagsBox.addItems(sorted(tags))

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.mainUpperLayout = QHBoxLayout()
        self.mainLowerLayout = QVBoxLayout()

        self.coursesLayout = QHBoxLayout()
        self.coursesLeftLayout = QHBoxLayout()
        self.coursesRightLayout = QVBoxLayout()
        self.coursesGroupBox = QGroupBox('Informations')
        self.coursesGroupBox.setFont(QFont("Times", 10, weight=QFont.Bold))

        self.schoolsLayout = QHBoxLayout()
        self.schoolsLeftLayout = QHBoxLayout()
        self.schoolsRightTopLayout = QHBoxLayout()
        self.schoolsRightBottomLayout = QHBoxLayout()
        self.schoolMainRightLayout = QVBoxLayout()
        self.schoolsGroupBox = QGroupBox('Search Schools')
        self.schoolsGroupBox2 = QGroupBox('School Informations')
        self.schoolsGroupBox.setFont(QFont("Times", 10, weight=QFont.Bold))
        self.schoolsGroupBox2.setFont(QFont("Times", 10, weight=QFont.Bold))

        self.instructorsLayout = QHBoxLayout()
        self.instructorsLeftLayout = QHBoxLayout()
        self.instructorsRightMainLayout = QVBoxLayout()
        self.instructorsRightTopLayout = QHBoxLayout()
        self.instructorsRightBottomLayout = QHBoxLayout()
        self.instructorsGroupBox = QGroupBox('Search Instructors')
        self.instructorsGroupBox.setFont(QFont("Times", 10, weight=QFont.Bold))
        self.instructorsGroupBox2 = QGroupBox('Instructor Informations')
        self.instructorsGroupBox2.setFont(QFont("Times", 10, weight=QFont.Bold))

        self.mainLayout.addLayout(self.mainUpperLayout)
        self.mainLayout.addLayout(self.mainLowerLayout)

        self.coursesGroupBox.setLayout(self.coursesRightLayout)
        self.coursesLayout.addLayout(self.coursesLeftLayout, 75)
        self.coursesLayout.addLayout(self.coursesRightLayout, 25)
        self.coursesLayout.addWidget(self.coursesGroupBox)
        self.coursesLeftLayout.addWidget(self.coursesTable)
        self.coursesRightLayout.addWidget(self.coursesInfo)

        self.schoolsLayout.addLayout(self.schoolsLeftLayout, 80)
        self.schoolsLayout.addLayout(self.schoolMainRightLayout, 20)
        self.schoolsLeftLayout.addWidget(self.schoolsTable)
        self.schoolsRightTopLayout.addWidget(self.schoolsSearchText)
        self.schoolsRightTopLayout.addWidget(self.schoolsSearchEntry)
        self.schoolsRightTopLayout.addWidget(self.schoolsSearchButton)
        self.schoolsGroupBox.setLayout(self.schoolsRightTopLayout)
        self.schoolsRightBottomLayout.addWidget(self.schoolsInfos)
        self.schoolsGroupBox2.setLayout(self.schoolsRightBottomLayout)
        self.schoolMainRightLayout.addWidget(self.schoolsGroupBox)
        self.schoolMainRightLayout.addWidget(self.schoolsGroupBox2)

        self.instructorsLayout.addLayout(self.instructorsLeftLayout, 80)
        self.instructorsLayout.addLayout(self.instructorsRightMainLayout, 20)
        self.instructorsLeftLayout.addWidget(self.instructorsTable)
        self.instructorsRightTopLayout.addWidget(self.instructorsSearchText)
        self.instructorsRightTopLayout.addWidget(self.instructorsSearchEntry)
        self.instructorsRightTopLayout.addWidget(self.instructorsSearchButton)
        self.instructorsGroupBox.setLayout(self.instructorsRightTopLayout)
        self.instructorsRightBottomLayout.addWidget(self.instructorsInfos)
        self.instructorsGroupBox2.setLayout(self.instructorsRightBottomLayout)
        self.instructorsRightMainLayout.addWidget(self.instructorsGroupBox)
        self.instructorsRightMainLayout.addWidget(self.instructorsGroupBox2)

        self.widget = QWidget()
        self.widget.setLayout(self.mainLayout)
        self.setCentralWidget(self.widget)

    def widgets(self):
        self.coursesTable = QTableWidget()
        self.coursesTable.setColumnCount(12)
        self.coursesTable.setColumnHidden(7, True)
        self.coursesTable.setColumnHidden(8, True)
        self.coursesTable.setColumnHidden(9, True)
        self.coursesTable.setColumnHidden(10, True)
        self.coursesTable.setColumnHidden(11, True)
        self.coursesTable.setHorizontalHeaderItem(0, QTableWidgetItem('Title'))
        self.coursesTable.setHorizontalHeaderItem(1, QTableWidgetItem('School'))
        self.coursesTable.setHorizontalHeaderItem(2, QTableWidgetItem('Instructor'))
        self.coursesTable.setHorizontalHeaderItem(3, QTableWidgetItem('Category'))
        self.coursesTable.setHorizontalHeaderItem(4, QTableWidgetItem('Duration'))
        self.coursesTable.setHorizontalHeaderItem(5, QTableWidgetItem('Directory'))
        self.coursesTable.setHorizontalHeaderItem(6, QTableWidgetItem('State'))
        self.coursesTable.setHorizontalHeaderItem(7, QTableWidgetItem('ID'))
        self.coursesTable.setHorizontalHeaderItem(8, QTableWidgetItem('SchoolID'))
        self.coursesTable.setHorizontalHeaderItem(9, QTableWidgetItem('InstructorID'))
        self.coursesTable.setHorizontalHeaderItem(10, QTableWidgetItem('Tags'))
        self.coursesTable.setHorizontalHeaderItem(11, QTableWidgetItem('Link'))
        self.coursesTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.coursesTable.horizontalHeader().setStretchLastSection(True)
        self.coursesTable.horizontalHeader().setFont(QFont("Times", weight=QFont.Bold))
        self.coursesTable.resizeColumnsToContents()
        self.coursesTable.setSortingEnabled(True)
        self.coursesTable.horizontalHeader().sortIndicatorOrder()
        self.coursesTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.coursesTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.coursesTable.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.coursesTable.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.coursesTable.doubleClicked.connect(self.selectedCourse)
        self.coursesTable.clicked.connect(self.showDetails)

        self.coursesInfo = QTextEdit()
        self.coursesInfo.setHtml(self.getBasicInfo())
        self.coursesInfo.setReadOnly(True)

        self.schoolsTable = QTableWidget()
        self.schoolsTable.setColumnCount(4)
        self.schoolsTable.setColumnHidden(0, True)
        self.schoolsTable.setHorizontalHeaderItem(0, QTableWidgetItem('ID'))
        self.schoolsTable.setHorizontalHeaderItem(1, QTableWidgetItem('Name'))
        self.schoolsTable.setHorizontalHeaderItem(2, QTableWidgetItem('Website'))
        self.schoolsTable.setHorizontalHeaderItem(3, QTableWidgetItem('Courses Count'))
        self.schoolsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.schoolsTable.horizontalHeader().setFont(QFont("Times", weight=QFont.Bold))
        self.schoolsTable.resizeColumnsToContents()
        self.schoolsTable.setSortingEnabled(True)
        self.schoolsTable.horizontalHeader().sortIndicatorOrder()
        self.schoolsTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.schoolsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.schoolsTable.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.schoolsTable.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.schoolsTable.doubleClicked.connect(self.selectedSchool)
        self.schoolsTable.clicked.connect(self.showSchoolDetails)
        self.schoolsSearchText = QLabel("Search School")
        self.schoolsSearchEntry = QLineEdit()
        self.schoolsSearchEntry.setPlaceholderText('Enter School name')
        self.schoolsSearchEntry.setCompleter(self.get_completer(schools, self.schoolsSearchEntry))
        self.schoolsSearchEntry.textEdited.connect(self.searchSchool)
        self.schoolsSearchEntry.returnPressed.connect(self.searchSchool)
        self.schoolsSearchButton = QPushButton("Search")
        self.schoolsSearchButton.clicked.connect(self.searchSchool)
        self.schoolsInfos = QTextEdit()
        self.schoolsInfos.setText(self.getSchoolsInfo())

        self.instructorsTable = QTableWidget()
        self.instructorsTable.setColumnCount(4)
        self.instructorsTable.setColumnHidden(0, True)
        self.instructorsTable.setHorizontalHeaderItem(0, QTableWidgetItem('ID'))
        self.instructorsTable.setHorizontalHeaderItem(1, QTableWidgetItem('Name'))
        self.instructorsTable.setHorizontalHeaderItem(2, QTableWidgetItem('School'))
        self.instructorsTable.setHorizontalHeaderItem(3, QTableWidgetItem('Courses Count'))
        self.instructorsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.instructorsTable.horizontalHeader().setFont(QFont("Times", weight=QFont.Bold))
        self.instructorsTable.resizeColumnsToContents()
        self.instructorsTable.setSortingEnabled(True)
        self.instructorsTable.horizontalHeader().sortIndicatorOrder()
        self.instructorsTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.instructorsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.instructorsTable.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.instructorsTable.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.instructorsTable.doubleClicked.connect(self.selectedInstructor)
        self.instructorsTable.clicked.connect(self.showInstructorDetails)
        self.instructorsSearchText = QLabel("Search Instructor")
        self.instructorsSearchEntry = QLineEdit()
        self.instructorsSearchEntry.setPlaceholderText('Enter Instructor name')
        self.instructorsSearchEntry.setCompleter(self.get_completer(instructors, self.instructorsSearchEntry))
        self.instructorsSearchEntry.textEdited.connect(self.searchInstructor)
        self.instructorsSearchEntry.returnPressed.connect(self.searchInstructor)
        self.instructorsSearchButton = QPushButton("Search")
        self.instructorsSearchButton.clicked.connect(self.searchInstructor)
        self.instructorsInfos = QTextEdit()
        self.instructorsInfos.setText(self.getInstructorsInfo())

    def funcAddCourse(self):
        self.newCourse = addcourse.AddCourse()
        self.get_Defaults()

    def funcAddSchool(self):
        self.newSchool = addschool.AddSchool()
        self.get_Defaults()

    def funcSettings(self):
        self.newSettings = settings.Settings()
        self.get_Defaults()

    def funcAddInstructor(self):
        self.newInstructor = addinstructor.AddInstructor()
        self.get_Defaults()

    def displayCourses(self):
        for i in reversed(range(self.coursesTable.rowCount())):
            self.coursesTable.removeRow(i)

        query = curr.execute(
            "SELECT Title,School.Name,Instructor.Name,Category,Duration,Directory,IsCompleted,course.ID,course.SchoolID,InstructorID,tags,course.link FROM course,instructor,school WHERE  course.InstructorID = instructor.ID and course.SchoolID = school.ID")

        oldSort = self.coursesTable.horizontalHeader().sortIndicatorSection()
        oldOrder = self.coursesTable.horizontalHeader().sortIndicatorOrder()
        self.coursesTable.setSortingEnabled(False)

        for row_data in query:
            row_number = self.coursesTable.rowCount()
            self.coursesTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem()
                item.setData(Qt.EditRole, data)
                if column_number != 0:
                    item.setTextAlignment(Qt.AlignCenter)
                self.coursesTable.setItem(row_number, column_number, item)
        self.coursesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.coursesTable.sortItems(oldSort, oldOrder)
        self.coursesTable.setSortingEnabled(True)

    def displaySchools(self):
        oldSort = self.schoolsTable.horizontalHeader().sortIndicatorSection()
        oldOrder = self.schoolsTable.horizontalHeader().sortIndicatorOrder()
        self.schoolsTable.setSortingEnabled(False)

        for i in reversed(range(self.schoolsTable.rowCount())):
            self.schoolsTable.removeRow(i)

        query = curr.execute(
            "SELECT ID,Name,Website,CourseCount FROM school")

        for row_data in query:
            row_number = self.schoolsTable.rowCount()
            self.schoolsTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem()
                item.setData(Qt.EditRole, data)
                item.setTextAlignment(Qt.AlignCenter)
                self.schoolsTable.setItem(row_number, column_number, item)
        self.schoolsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.schoolsTable.sortItems(oldSort, oldOrder)
        self.schoolsTable.setSortingEnabled(True)

    def displayInstructors(self):
        oldSort = self.instructorsTable.horizontalHeader().sortIndicatorSection()
        oldOrder = self.instructorsTable.horizontalHeader().sortIndicatorOrder()
        self.instructorsTable.setSortingEnabled(False)

        for i in reversed(range(self.instructorsTable.rowCount())):
            self.instructorsTable.removeRow(i)

        query = curr.execute(
            "SELECT Instructor.ID,Instructor.Name,School.Name,CoursesCount FROM school,Instructor WHERE SchoolID=School.ID")

        for row_data in query:
            row_number = self.instructorsTable.rowCount()
            self.instructorsTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem()
                item.setData(Qt.EditRole, data)
                item.setTextAlignment(Qt.AlignCenter)
                self.instructorsTable.setItem(row_number, column_number, item)
        self.instructorsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.instructorsTable.sortItems(oldSort, oldOrder)
        self.instructorsTable.setSortingEnabled(True)

    def selectedCourse(self):
        global courseID
        listProduct = []

        for i in range(0, 12):
            try:
                listProduct.append(self.coursesTable.item(self.coursesTable.currentRow(), i).text())
            except Exception as e:
                print(e)
                QMessageBox.information(self, 'Informations', e)

        courseID = listProduct[7]
        try:
            self.display = DisplayCourse()
        except Exception as e:
            print(e)
            QMessageBox.information(self, 'Informations', e)
        self.display.show()

    def selectedSchool(self):
        global schoolID
        listSchools = []
        for i in range(0, 4):
            listSchools.append(self.schoolsTable.item(self.schoolsTable.currentRow(), i).text())
        schoolID = listSchools[0]
        try:
            self.displaySchool = DisplaySchool()
        except Exception as e:
            QMessageBox.information(self, 'Informations', e)
        self.displaySchool.show()

    def selectedInstructor(self):
        global instructorID
        listInstructor = []
        for i in range(0, 4):
            listInstructor.append(self.instructorsTable.item(self.instructorsTable.currentRow(), i).text())
        instructorID = listInstructor[0]
        try:
            self.displayInstructor = DisplayInstructor()
        except Exception as e:
            QMessageBox.information(self, 'Informations', e)
        self.displayInstructor.show()

    def get_Defaults(self):
        global schools
        global instructors
        global categories
        global all_courses
        global tags
        s = curr.execute('SELECT DISTINCT Name FROM School')
        schools = [i[0] for i in s]
        i = curr.execute('SELECT DISTINCT Name FROM Instructor')
        instructors = [j[0] for j in i]
        c = curr.execute('SELECT DISTINCT Category FROM Course')
        categories = [i[0] for i in c]
        a = curr.execute('SELECT DISTINCT Title FROM Course')
        all_courses = [i[0] for i in a]
        t = curr.execute('SELECT Tags FROM Course')
        tags = [i[0].split(',') for i in t]
        tags = {j for i in tags for j in i}
        tags.remove('')

    def filter(self):
        self.get_Defaults()
        try:
            school = self.schoolCombo.currentText().replace("'", "''")
            category = self.categoryCombo.currentText().replace("'", "''")
            instructor = self.instructorBox.currentText().replace("'", "''")
            state = self.iscompletedCombo.currentText().replace("'", "''")
            directory = self.directoryCombo.currentText().replace("'", "''")
            tag = self.tagsBox.currentText().replace("'", "''").split(',')
            all_schools, all_category, all_instructors, all_states, all_directory, all_tags = [], [], [], [], [], []

            if (school != 'Schools'):
                try:
                    q1 = curr.execute("select ID from school where name =?", (school,))
                    index = curr.fetchone()[0]
                    all_schools = curr.execute(
                        "SELECT Title,School.Name,Instructor.Name,Category,Duration,Directory,IsCompleted,course.ID,course.SchoolID,InstructorID,tags,course.link FROM course,instructor,school WHERE course.InstructorID = instructor.ID and course.SchoolID = school.ID and course.schoolID = ?",
                        (index,))
                    all_schools = curr.fetchall()
                except Exception as e:
                    QMessageBox.information(self, 'information', 'items does not exist')

            if (category != 'Category'):
                try:
                    all_category = curr.execute(
                        "SELECT Title,School.Name,Instructor.Name,Category,Duration,Directory,IsCompleted,course.ID,course.SchoolID,InstructorID,tags,course.link FROM course,instructor,school WHERE course.InstructorID = instructor.ID and course.SchoolID = school.ID and category = ?",
                        (category,))
                    all_category = curr.fetchall()
                except Exception as e:
                    QMessageBox.information(self, 'information', 'items does not exist')

            if (instructor != 'Instructors'):
                try:
                    q1 = curr.execute("select ID from Instructor where name =?", (instructor,))
                    index = curr.fetchone()[0]
                    all_instructors = curr.execute(
                        "SELECT Title,School.Name,Instructor.Name,Category,Duration,Directory,IsCompleted,course.ID,course.SchoolID,InstructorID,tags,course.link FROM course,instructor,school WHERE course.InstructorID = instructor.ID and course.SchoolID = school.ID and course.InstructorID = ?",
                        (index,))
                    all_instructors = curr.fetchall()
                except Exception as e:
                    QMessageBox.information(self, 'information', 'items does not exist')

            if (state != 'State'):
                try:
                    all_states = curr.execute(
                        "SELECT Title,School.Name,Instructor.Name,Category,Duration,Directory,IsCompleted,course.ID,course.SchoolID,InstructorID,tags,course.link FROM course,instructor,school WHERE course.InstructorID = instructor.ID and course.SchoolID = school.ID and IsCompleted=?",
                        (state,))
                    all_states = curr.fetchall()
                except Exception as e:
                    QMessageBox.information(self, 'Informations', e)

            if (directory != 'Directory'):
                try:
                    all_directory = curr.execute(
                        "SELECT Title,School.Name,Instructor.Name,Category,Duration,Directory,IsCompleted,course.ID,course.SchoolID,InstructorID,tags,course.link FROM course,instructor,school WHERE course.InstructorID = instructor.ID and course.SchoolID = school.ID and directory = ?",
                        (directory,))
                    all_directory = curr.fetchall()
                except Exception as e:
                    QMessageBox.information(self, 'information', 'items does not exist')
            all_tags = []
            if (tag != [] and tag[0] != 'Tags'):
                try:
                    for t in tag:
                        _ = curr.execute(
                            "SELECT Title,School.Name,Instructor.Name,Category,Duration,Directory,IsCompleted,course.ID,course.SchoolID,InstructorID,tags,course.link FROM course,instructor,school WHERE course.InstructorID = instructor.ID and course.SchoolID = school.ID and Tags Like '%'||?||'%'",
                            (t,))
                        all_tags.extend(curr.fetchall())
                except Exception as e:
                    QMessageBox.information(self, 'information', 'items does not exist')
            if any(
                    [all_schools, all_category, all_instructors, all_states, all_directory, all_tags]):
                all = set.intersection(
                    *(set(x) for x in [all_schools, all_category, all_instructors, all_states, all_directory, all_tags]
                      if
                      x))

                oldSort = self.coursesTable.horizontalHeader().sortIndicatorSection()
                oldOrder = self.coursesTable.horizontalHeader().sortIndicatorOrder()
                self.coursesTable.setSortingEnabled(False)

                for i in reversed(range(self.coursesTable.rowCount())):
                    self.coursesTable.removeRow(i)

                for row_data in all:
                    row_number = self.coursesTable.rowCount()
                    self.coursesTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        item = QTableWidgetItem()
                        item.setData(Qt.EditRole, data)
                        if column_number != 0:
                            item.setTextAlignment(Qt.AlignCenter)
                        self.coursesTable.setItem(row_number, column_number, item)
                self.coursesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.coursesTable.sortItems(oldSort, oldOrder)
                self.coursesTable.setSortingEnabled(True)
            else:
                self.displayCourses()

        except Exception as e:
            QMessageBox.information(self, 'Informations', e)

    def get_completer(self, text, searchEntry):
        completer = QCompleter(text, searchEntry)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setFilterMode(Qt.MatchContains)
        completer.setMaxVisibleItems(20)
        completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
        return completer

    def searchCourse(self):
        value = self.searchBox.text()
        if value != "":
            try:
                value = value.replace("'", "''")
                query = curr.execute(
                    f"SELECT Title,School.Name,Instructor.Name,Category,Duration,Directory,IsCompleted,course.ID,course.SchoolID,InstructorID,tags,course.link FROM course,instructor,school WHERE course.InstructorID = instructor.ID and course.SchoolID = school.ID and Title LIKE '%{value}%'")
            except Exception as e:
                QMessageBox.information(self, 'Informations', e)

            oldSort = self.coursesTable.horizontalHeader().sortIndicatorSection()
            oldOrder = self.coursesTable.horizontalHeader().sortIndicatorOrder()
            self.coursesTable.setSortingEnabled(False)

            for i in reversed(range(self.coursesTable.rowCount())):
                self.coursesTable.removeRow(i)

            for row_data in query:
                row_number = self.coursesTable.rowCount()
                self.coursesTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem()
                    item.setData(Qt.EditRole, data)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.coursesTable.setItem(row_number, column_number, item)
            self.coursesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.coursesTable.sortItems(oldSort, oldOrder)
            self.coursesTable.setSortingEnabled(True)
        else:
            self.displayCourses()

    def searchSchool(self):
        value = self.schoolsSearchEntry.text()
        if value:
            try:
                value = value.replace("'", "''")
                query = curr.execute(
                    f"SELECT ID,Name,Website,CourseCount FROM school WHERE Name LIKE '%{value}%'")
            except Exception as e:
                QMessageBox.information(self, 'Informations', e)

            oldSort = self.schoolsTable.horizontalHeader().sortIndicatorSection()
            oldOrder = self.schoolsTable.horizontalHeader().sortIndicatorOrder()
            self.schoolsTable.setSortingEnabled(False)

            for i in reversed(range(self.schoolsTable.rowCount())):
                self.schoolsTable.removeRow(i)

            for row_data in query:
                row_number = self.schoolsTable.rowCount()
                self.schoolsTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem()
                    item.setData(Qt.EditRole, data)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.schoolsTable.setItem(row_number, column_number, item)
            self.schoolsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.schoolsTable.sortItems(oldSort, oldOrder)
            self.schoolsTable.setSortingEnabled(True)
        else:
            self.displaySchools()

    def searchInstructor(self):
        value = self.instructorsSearchEntry.text()
        if value != "":
            try:
                value = value.replace("'", "''")
                query = curr.execute(
                    f"SELECT Instructor.ID,Instructor.Name,School.Name,CoursesCount FROM school,Instructor WHERE SchoolID=School.ID and Instructor.Name LIKE '%{value}%'")
            except Exception as e:
                QMessageBox.information(self, 'Informations', e)

            oldSort = self.instructorsTable.horizontalHeader().sortIndicatorSection()
            oldOrder = self.instructorsTable.horizontalHeader().sortIndicatorOrder()
            self.instructorsTable.setSortingEnabled(False)

            for i in reversed(range(self.instructorsTable.rowCount())):
                self.instructorsTable.removeRow(i)

            for row_data in query:
                row_number = self.instructorsTable.rowCount()
                self.instructorsTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem()
                    item.setData(Qt.EditRole, data)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.instructorsTable.setItem(row_number, column_number, item)
            self.instructorsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.instructorsTable.sortItems(oldSort, oldOrder)
            self.instructorsTable.setSortingEnabled(True)
        else:
            self.displayInstructors()

    def showDetails(self):
        listProduct = []

        for i in range(0, 12):  # Should be 10 not 9
            try:
                listProduct.append(self.coursesTable.item(self.coursesTable.currentRow(), i).text())
            except Exception as e:
                QMessageBox.information(self, 'Informations', e)
        dir = ""
        if listProduct[5] == '1':
            dir = 'First drive'
        elif listProduct[5] == '2':
            dir = 'Second drive'
        elif listProduct[5] == '3':
            dir = 'Third drive'
        else:
            dir = 'Online School'
        self.coursesInfo.setHtml(
            f"<br/><br/><br/>Course Title is:<font color=#0D7EDD> <br/> {listProduct[0]} <br/><br/> <font color=#000000> The course is from: <font color=#0D7EDD> <br/> {listProduct[1]} <br/><br/> <font color=#000000> The Instructor is: <font color=#0D7EDD> <br/> {listProduct[2]} <br/><br/> <font color=#000000> This Course Belongs to: <font color=#0D7EDD> <br/> {listProduct[3]} <br/><br/> <font color=#000000> This Course Is: <font color=#0D7EDD> <br/> {listProduct[6]} <br/> <font color=#000000> and it is located in the <font color=#0D7EDD> <br/> {dir} <br/><br/> <font color=#000000> The duration of the course is: <font color=#0D7EDD> <br/> {listProduct[4]} <br/><br/> <font color=#000000> Course Tags are: <font color=#0D7EDD> <br/> {listProduct[10]} <br/><br/> <font color=#000000> Course Link: <font color=#0D7EDD> <br/> {listProduct[11]}")

    def showSchoolDetails(self):
        listSchools = []
        for i in range(0, 4):
            listSchools.append(self.schoolsTable.item(self.schoolsTable.currentRow(), i).text())

        self.schoolsInfos.setHtml(
            f"<br/><br/><br/>School Name is:<font color=#0D7EDD> <br/> {listSchools[1]} <br/><br/> <font color=#000000> The link to the school is: <font color=#0D7EDD> <br/> {listSchools[2]} <br/><br/> <font color=#000000> And has <font color=#0D7EDD>{listSchools[3]} <font color=#000000> Courses.")

    def showInstructorDetails(self):
        listSchools = []
        for i in range(0, 4):
            listSchools.append(self.instructorsTable.item(self.instructorsTable.currentRow(), i).text())
        self.instructorsInfos.setHtml(
            f"<br/><br/><br/>Instructor Name is:<font color=#0D7EDD> <br/> {listSchools[1]} <br/><br/> <font color=#000000> The instructor teaches at: <font color=#0D7EDD> <br/> {listSchools[2]} <br/><br/> <font color=#000000> And has <font color=#0D7EDD>{listSchools[3]} <font color=#000000> Courses.")

    def getBasicInfo(self):
        def calculate_duration(prv, nex):
            h1, m1, s1 = map(int, prv.split(':'))
            h2, m2, s2 = map(int, nex.split(':'))

            h = h1 + h2
            m = m1 + m2
            s = s1 + s2
            if s >= 60:
                s %= 60
                m += 1
            if m >= 60:
                m %= 60
                h += 1
            h = '0' + str(h) if h <= 9 else h
            m = '0' + str(m) if m <= 9 else m
            s = '0' + str(s) if s <= 9 else s
            return f'{h}:{m}:{s}'

        courses_count = curr.execute('select count(*) from course')
        courses_count = curr.fetchone()[0]
        schools_count = curr.execute('select count(*) from school')
        schools_count = curr.fetchone()[0]
        instructors_count = curr.execute('select count(*) from instructor')
        instructors_count = curr.fetchone()[0]

        q = curr.execute('SELECT duration from course')
        duration = '00:00:00'
        for d in q:
            duration = calculate_duration(duration, d[0])
        return f"<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>You Have <font color=#0D7EDD> {courses_count} <font color=#000000> Course From <font color=#0D7EDD>  {schools_count} <font color=#000000> School and  <font color=#0D7EDD> {instructors_count} <font color=#000000>Instructor.<br/><br/><br/> The total duration of the courses is <font color=#0D7EDD>{duration}<font color=#000000> Hour"

    def getSchoolsInfo(self):
        schools_count = curr.execute('select count(*) from school')
        schools_count = curr.fetchone()[0]
        order_schools = curr.execute('select Name,courseCount from school order by courseCount DESC')
        orders = curr.fetchmany(5)
        return f"<br/><br/><br/><br/><br/><br/>You Have <font color=#0D7EDD> {schools_count} <font color=#000000> Schools. <br/><br/><br/> The first five schools with the biggest number of courses are ordered from: <font color=#0D7EDD><br/> - {orders[0][0]}<font color=#000000> With a total of <font color=#0D7EDD>{orders[0][1]} courses <font color=#0D7EDD><br/> - {orders[1][0]}<font color=#000000> With a total of <font color=#0D7EDD>{orders[1][1]} courses<font color=#0D7EDD><br/> - {orders[2][0]}<font color=#000000> With a total of <font color=#0D7EDD>{orders[2][1]} courses <font color=#0D7EDD><br/> - {orders[3][0]}<font color=#000000> With a total of <font color=#0D7EDD>{orders[3][1]} courses<font color=#0D7EDD><br/> - {orders[4][0]}<font color=#000000> With a total of <font color=#0D7EDD>{orders[4][1]} courses"

    def getInstructorsInfo(self):
        schools_count = curr.execute('select count(*) from instructor')
        schools_count = curr.fetchone()[0]
        order_schools = curr.execute('select Name,coursesCount from instructor order by coursesCount DESC')
        orders = curr.fetchmany(5)
        return f"<br/><br/><br/><br/><br/><br/>You Have <font color=#0D7EDD> {schools_count} <font color=#000000> Schools. <br/><br/><br/> The first five instructors with the biggest number of courses are ordered from: <font color=#0D7EDD><br/> - {orders[0][0]}<font color=#000000> With a total of <font color=#0D7EDD>{orders[0][1]} courses <font color=#0D7EDD><br/> - {orders[1][0]}<font color=#000000> With a total of <font color=#0D7EDD>{orders[1][1]} courses<font color=#0D7EDD><br/> - {orders[2][0]}<font color=#000000> With a total of <font color=#0D7EDD>{orders[2][1]} courses <font color=#0D7EDD><br/> - {orders[3][0]}<font color=#000000> With a total of <font color=#0D7EDD>{orders[3][1]} courses<font color=#0D7EDD><br/> - {orders[4][0]}<font color=#000000> With a total of <font color=#0D7EDD>{orders[4][1]} courses"


class DisplayInstructor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'Instructor Detail')
        self.setGeometry(450, 100, 350, 550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.instructorDetails()
        try:
            self.widgets()
        except Exception as e:
            QMessageBox.information(self, 'Informations', e)
        self.layouts()

    def instructorDetails(self):
        global instructorID
        try:
            query = 'SELECT Instructor.Name,CoursesCount,School.name FROM Instructor,School WHERE Instructor.ID=? and School.ID = SchoolID'
            instructor = curr.execute(query, (instructorID,)).fetchone()
        except Exception as e:
            QMessageBox.information(self, 'Informations', e)
        self.instructorName = instructor[0]
        self.instructorCourses = instructor[1]
        self.instructorSchool = instructor[2]

    def widgets(self):
        self.titleText = QLabel("Update Instructor")
        self.titleText.setFont(QFont("SansSerif", 20))
        self.titleText.setAlignment(Qt.AlignCenter)

        self.nameEntry = QLineEdit()
        self.nameEntry.setText(self.instructorName)
        self.schoolEntry = QLineEdit()
        self.schoolEntry.setText(self.instructorSchool)
        self.coursescountEntry = QLineEdit()
        self.coursescountEntry.setText(str(self.instructorCourses))
        self.deleteBtn = QPushButton('Delete')
        self.deleteBtn.clicked.connect(self.deleteInstructor)
        self.updateBtn = QPushButton('Update')
        self.updateBtn.clicked.connect(self.updateInstructor)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)
        self.bottomLayout.addRow(QLabel('Name: '), self.nameEntry)
        self.bottomLayout.addRow(QLabel('School: '), self.schoolEntry)
        self.bottomLayout.addRow(QLabel('Courses Count: '), self.coursescountEntry)
        self.bottomLayout.addRow(QLabel(''), self.updateBtn)
        self.bottomLayout.addRow(QLabel(''), self.deleteBtn)

        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def updateInstructor(self):
        try:
            schoolName = self.schoolEntry.text().replace("'", "''")
            instructorName = self.nameEntry.text().replace("'", "''")
            instructorCount = self.coursescountEntry.text().replace("'", "''")
        except Exception as e:
            QMessageBox.information(self, 'Informations', e)

        if (schoolName and instructorName and instructorCount):
            try:
                query = "UPDATE Instructor SET Name=?,CoursesCount=?,SchoolID=? WHERE ID=?"
                q = "SELECT ID FROM school WHERE Name=?"
                curr.execute(q, (schoolName,))
                id = curr.fetchone()[0]
                curr.execute(query, (instructorName, instructorCount, id, instructorID))
                conn.commit()
                QMessageBox.information(self, 'Info', 'School has been updated Successfully')
                self.close()
            except Exception as e:
                QMessageBox.information(self, 'Info', 'School has not been updated Successfully')
        else:
            QMessageBox.information(self, 'Info', "Fields can't be empty")

    def deleteInstructor(self):
        global schoolID

        mbox = QMessageBox.question(self, "Warning", "Are you sure to delete this school?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if mbox == QMessageBox.Yes:
            try:
                curr.execute('DELETE FROM Instructor WHERE ID=?', (instructorID,))
                conn.commit()
                QMessageBox.information(self, 'Info', 'School has been deleted')
                self.close()
            except:
                QMessageBox.information(self, 'Info', 'School has not been deleted')


class DisplaySchool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'School Detail')
        self.setGeometry(450, 100, 350, 550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.schoolDetails()
        try:
            self.widgets()
        except Exception as e:
            QMessageBox.information(self, 'Informations', e)
        self.layouts()

    def schoolDetails(self):
        global schoolID
        try:
            query = 'SELECT Name,Website,CourseCount FROM school WHERE ID=?'
            school = curr.execute(query, (schoolID,)).fetchone()
        except Exception as e:
            QMessageBox.information(self, 'Informations', e)
        self.schoolName = school[0]
        self.schoolLink = school[1]
        self.schoolCourses = school[2]

    def widgets(self):
        self.titleText = QLabel("Update School")
        self.titleText.setFont(QFont("SansSerif", 20))
        self.titleText.setAlignment(Qt.AlignCenter)

        self.nameEntry = QLineEdit()
        self.nameEntry.setText(self.schoolName)
        self.linkEntry = QLineEdit()
        self.linkEntry.setText(self.schoolLink)
        self.coursescountEntry = QLineEdit()
        self.coursescountEntry.setText(str(self.schoolCourses))
        self.deleteBtn = QPushButton('Delete')
        self.deleteBtn.clicked.connect(self.deleteSchool)
        self.updateBtn = QPushButton('Update')
        self.updateBtn.clicked.connect(self.updateSchool)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)
        self.bottomLayout.addRow(QLabel('Name: '), self.nameEntry)
        self.bottomLayout.addRow(QLabel('Link: '), self.linkEntry)
        self.bottomLayout.addRow(QLabel('Courses Count: '), self.coursescountEntry)
        self.bottomLayout.addRow(QLabel(''), self.updateBtn)
        self.bottomLayout.addRow(QLabel(''), self.deleteBtn)

        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def updateSchool(self):
        try:
            schoolName = self.nameEntry.text().replace("'", "''")
            schoolLink = self.linkEntry.text().replace("'", "''")
            schoolCount = self.coursescountEntry.text().replace("'", "''")
        except Exception as e:
            QMessageBox.information(self, 'Informations', e)

        if (schoolName and schoolLink and schoolCount):
            try:
                query = "UPDATE school SET Name=?,Website=?,CourseCount=? WHERE ID=?"
                curr.execute(query, (schoolName, schoolLink, schoolCount, schoolID))
                conn.commit()
                QMessageBox.information(self, 'Info', 'School has been updated Successfully')
                self.close()
            except Exception as e:
                QMessageBox.information(self, 'Info', 'School has not been updated Successfully')
        else:
            QMessageBox.information(self, 'Info', "Fields can't be empty")

    def deleteSchool(self):
        global schoolID

        mbox = QMessageBox.question(self, "Warning", "Are you sure to delete this school?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if mbox == QMessageBox.Yes:
            try:
                curr.execute('DELETE FROM school WHERE ID=?', (schoolID,))
                conn.commit()
                QMessageBox.information(self, 'Info', 'School has been deleted')
                self.close()
            except:
                QMessageBox.information(self, 'Info', 'School has not been deleted')


class DisplayCourse(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'Course Detail')
        self.setGeometry(450, 100, 350, 550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.courseDetails()
        try:
            self.widgets()
        except Exception as e:
            QMessageBox.information(self, 'Informations', e)
        self.layouts()

    def courseDetails(self):
        global courseID
        try:
            query = 'SELECT Title,School.Name,Instructor.Name,Category,Duration,Directory,IsCompleted,Tags,Link FROM course,instructor,school WHERE course.schoolID = school.ID and instructor.ID = course.instructorID and course.ID=?'
            course = curr.execute(query, (courseID,)).fetchone()
        except Exception as e:
            QMessageBox.information(self, 'Informations', e)
        self.courseTitle = course[0]
        self.courseSchool = course[1]
        self.courseInstructor = course[2]
        self.courseCategory = course[3]
        self.courseDuration = course[4]
        self.courseDirectory = course[5]
        self.courseState = course[6]
        self.courseTags = course[7]
        self.courseLink = course[8]

    def widgets(self):
        self.titleText = QLabel("Update Course")
        self.titleText.setFont(QFont("SansSerif", 20))
        self.titleText.setAlignment(Qt.AlignCenter)

        self.titleEntry = QLineEdit()
        self.titleEntry.setText(self.courseTitle)
        self.durationEntry = QLineEdit()
        self.durationEntry.setText(self.courseDuration)
        self.tagsEntry = QLineEdit()
        self.tagsEntry.setText(self.courseTags)
        self.schoolEntry = ExtendedComboBox()
        self.schoolEntry.addItems(sorted(schools))
        self.schoolEntry.setCurrentText(self.courseSchool)
        self.instructorEntry = ExtendedComboBox()
        self.instructorEntry.addItems(sorted(instructors))
        self.instructorEntry.setCurrentText(self.courseInstructor)
        self.categoryEntry = ExtendedComboBox()
        self.categoryEntry.addItems(sorted(categories))
        self.categoryEntry.setCurrentText(self.courseCategory)
        self.directoryEntry = ExtendedComboBox()
        self.directoryEntry.addItems(['1', '2', '3'])
        self.directoryEntry.setCurrentText(self.courseDirectory)
        self.stateEntry = ExtendedComboBox()
        self.stateEntry.addItems(['Completed', 'Not Completed'])
        self.stateEntry.setCurrentText(self.courseState)
        self.linkEntry = QLineEdit()
        self.linkEntry.setText(self.courseLink)
        self.deleteBtn = QPushButton('Delete')
        self.deleteBtn.clicked.connect(self.deleteCourse)
        self.updateBtn = QPushButton('Update')
        self.updateBtn.clicked.connect(self.updateCourse)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)
        self.bottomLayout.addRow(QLabel('Title: '), self.titleEntry)
        self.bottomLayout.addRow(QLabel('School: '), self.schoolEntry)
        self.bottomLayout.addRow(QLabel('Instructor: '), self.instructorEntry)
        self.bottomLayout.addRow(QLabel('Link: '), self.linkEntry)
        self.bottomLayout.addRow(QLabel('Duration: '), self.durationEntry)
        self.bottomLayout.addRow(QLabel('Category: '), self.categoryEntry)
        self.bottomLayout.addRow(QLabel('Tags: '), self.tagsEntry)
        self.bottomLayout.addRow(QLabel('Directory: '), self.directoryEntry)
        self.bottomLayout.addRow(QLabel('State: '), self.stateEntry)
        self.bottomLayout.addRow(QLabel(''), self.updateBtn)
        self.bottomLayout.addRow(QLabel(''), self.deleteBtn)

        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def updateCourse(self):
        try:
            courseTitle = self.titleEntry.text().replace("'", "''")
            courseSchool = self.schoolEntry.currentText().replace("'", "''")
            courseInstructor = self.instructorEntry.currentText().replace("'", "''")
            courseCategory = self.categoryEntry.currentText().replace("'", "''")
            courseDuration = self.durationEntry.text().replace("'", "''")
            courseDirectory = self.directoryEntry.currentText().replace("'", "''")
            courseState = self.stateEntry.currentText().replace("'", "''")
            courseTags = self.tagsEntry.text().replace("'", "''")
            courseLink = self.linkEntry.text().replace("'", "''")
        except Exception as e:
            QMessageBox.information(self, 'Informations', e)

        if (
                courseTitle and courseDuration and courseState and courseTags and courseInstructor and courseDirectory and courseCategory and courseSchool and courseLink):
            try:
                query = "UPDATE course SET Title=?,SchoolID=?,InstructorID=?,Category=?,Duration=?,Directory=?,IsCompleted=?,Tags=?,Link=? WHERE ID=?"
                q = curr.execute('SELECT ID FROM School WHERE Name=?', (courseSchool,))
                s = q.fetchone()[0]
                q = curr.execute('SELECT ID FROM Instructor WHERE Name=?', (courseInstructor,))
                i = q.fetchone()[0]
                curr.execute(query, (
                    courseTitle, s, i, courseCategory, courseDuration, courseDirectory, courseState, courseTags,
                    courseLink,
                    courseID))
                conn.commit()
                QMessageBox.information(self, 'Info', 'Course has been updated Successfully')
                self.close()
            except Exception as e:
                QMessageBox.information(self, 'Informations', e)

        else:
            QMessageBox.information(self, 'Info', "Fields can't be empty")

    def deleteCourse(self):
        global courseID

        mbox = QMessageBox.question(self, "Warning", "Are you sure to delete this course?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if mbox == QMessageBox.Yes:
            try:
                curr.execute('DELETE FROM course WHERE ID=?', (courseID,))
                conn.commit()
                QMessageBox.information(self, 'Info', 'Course has been deleted')
                self.close()
            except:
                QMessageBox.information(self, 'Info', 'Course has not been deleted')


def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())


if __name__ == "__main__":
    main()
