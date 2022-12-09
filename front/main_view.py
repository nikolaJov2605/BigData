from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
import pandas

class MainWindow(QDialog):
    file = None
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("front/main_view.ui", self)
        self.browse_btn.clicked.connect(self.browse_files)
        self.convert_data_btn.clicked.connect(self.convert_data)

    def browse_files(self):
        self.file = QFileDialog.getOpenFileName(self, 'Open file', 'data', 'XLSX (*.xlsx)')
        self.filename.setText(self.file[0])
        if self.file is not None:
            self.convert_data_btn.setEnabled(True)
    
    def convert_data(self):
        if self.file is None:
            return
        
        filename = "data/" + self.filename.text().split('/')[-1]
        print("Filename: ", filename)
        weather_cols = ["Local time", "T", "Po", "P", "Pa", "U", "DD", "Ff", "N", "WW", "W1", "W2"]
        exc_weather = pandas.read_excel(filename, sheet_name='weather', usecols=weather_cols)
        exc_weather.to_csv("weather.csv", index = None, header = True)

        

