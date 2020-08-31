import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):
    # Override class constructor
    def __init__(self):
        # You must call the super class method
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(480, 80))  # Set sizes
        self.setWindowTitle("Line Edit IP Address")  # Set the window title
        central_widget = QWidget(self)  # Create a central widget
        self.setCentralWidget(central_widget)  # Install the central widget

        grid_layout = QGridLayout(self)  # Create QGridLayout
        central_widget.setLayout(grid_layout)  # Set this accommodation in central widget

        grid_layout.addWidget(QLabel("Autocompletion check", self), 0, 0)

        # Create an input field
        lineEdit = QLineEdit(self)
        strList = ['Python', 'PyQt5', 'Qt', 'Django', 'QML']  # Create a list of words
        # We create QCompleter, in which we establish the list, and also the pointer to the parent
        completer = QCompleter(strList, lineEdit)
        lineEdit.setCompleter(completer)  # Set QCompleter in the input field
        grid_layout.addWidget(lineEdit, 0, 1)  # Add the input field to the grid


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())