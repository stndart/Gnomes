from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class Sooqa(QLabel):
    def __init__(self, parent=None):
        super().__init__(self, parent)
        self.setFixedSize(500, 500)
        self.setPixmap(self.get_image())
        self.show()
    
    def get_image(self):
        return QPixmap()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sooqa = Sooqa()
    app.exec()