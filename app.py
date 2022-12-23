import sys
from front.main_view import MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
mainWindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedWidth(800)
widget.setFixedHeight(600)
widget.show()
sys.exit(app.exec_())