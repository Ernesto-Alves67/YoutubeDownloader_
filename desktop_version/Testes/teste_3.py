import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidget, QTableWidgetItem, QAction
from PyQt5 import QtCore
from ytgui import Ui_MainWindow
from PyQt5.QtCore import Qt, QEvent
from ytgui import Ui_MainWindow



class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())