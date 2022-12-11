import sys
import pandas
import numpy

from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from backend.data_converter import DataConverter
from backend.data_writer import DataWriter

class MainWindow(QDialog):
    file = None
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("front/main_view.ui", self)
        self.browse_btn.clicked.connect(self.browse_files)
        self.convert_data_btn.clicked.connect(self.load_to_database)

    def browse_files(self):
        self.file = QFileDialog.getOpenFileName(self, 'Open file', 'data', 'XLSX (*.xlsx)')
        self.filename.setText(self.file[0].split('/')[-1])
        if self.file is not None:
            self.convert_data_btn.setEnabled(True)
    
    def load_to_database(self):
        if self.file is None:
            return
        
        filename = "data/" + self.filename.text()#.split('/')[-1]
        print("Filename: ", filename)
        data_converter = DataConverter(filename)
        ret_data = data_converter.load_data()       # ret_data[0] = weather; ret_data[1] = load
        data_writer = DataWriter(ret_data)
        data_writer.write_to_database()
        #data_converter.write_data()
        print ("hello")
        

        

