import sys
import time
import pandas
import numpy

from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from backend.data_converter import DataConverter
from backend.data_preparer import DataPreparer
from backend.data_writer import DataWriter
from backend.ann_regression import AnnRegression
from backend.scorer import Scorer
from backend.plotting import Plotting

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
        print("\nLoading and converting data...")
        data_converter = DataConverter(filename)
        ret_data = data_converter.load_data()       # ret_data[0] = weather; ret_data[1] = load
        print("\nDone.")
        print("\nWriting to database...")
        data_writer = DataWriter(ret_data)
        data_writer.write_to_database()
        print("\nDone")
        
        print("\nPreparing data...")
        data_preparer = DataPreparer()
        trainX, trainY, testX, testY = data_preparer.prepare_for_training()
        print("\nDone.")

        print("Doing some learning...")
        ann_regression = AnnRegression()
        time_begin = time.time()
        trainPredict, testPredict = ann_regression.compile_fit_predict(trainX, trainY, testX)
        time_end = time.time()
        print('Training duration: ' + str((time_end - time_begin)) + 'seconds')

        trainPredict, trainY, testPredict, testY = data_preparer.inverse_transform(trainPredict, testPredict)


        print("\nCalculating error...")
        scorer = Scorer()
        trainScore, testScore = scorer.get_score(trainY, trainPredict, testY, testPredict)
        print('Train Score: %.2f RMSE' % (trainScore))
        print('Test Score: %.2f RMSE' % (testScore))

        custom_plotting = Plotting()
        custom_plotting.show_plots(testPredict, testY)