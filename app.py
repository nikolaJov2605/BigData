import sys
from front.main_view import MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
mainWindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedWidth(500)
widget.setFixedHeight(200)
widget.show()
sys.exit(app.exec_())