import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMainWindow
from PyQt5 import QtGui

class EjemploGui(QWidget):
    def __init__(self):
        super(EjemploGui, self).__init__()
        self.setWindowTitle("Ejemplo de GUI con PyQt")
        salir = QPushButton("Salir", self)
        salir.setGeometry(100,100,100,100)
        salir.clicked.connect(self.close)

app = QApplication(sys.argv)
my_app = EjemploGui()
my_app.show()
sys.exit(app.exec_())