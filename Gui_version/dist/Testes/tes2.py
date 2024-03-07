import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from novo2 import Ui_MainWindow
from PyQt5.QtCore import Qt


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())