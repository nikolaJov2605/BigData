import sys
import threading
import time
import pandas
import numpy
import pyqtgraph

from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from backend.data_converter import DataConverter
from backend.data_preparer import DataPreparer
from backend.data_writer import DataWriter
from backend.ann_regression import AnnRegression
from backend.scorer import Scorer
from backend.plotting import Plotting
from front.stream import Stream

class MainWindow(QDialog):
    file = None
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("front/main_view.ui", self)
        self.browse_btn.clicked.connect(self.browse_files)
        self.convert_data_btn.clicked.connect(self.load_to_database_thread)
        self.start_ann_btn.clicked.connect(self.start_ann_thread)


        sys.stdout = Stream(newText=self.onUpdateText)

        #x = threading.Thread(target=self.listen)
        #x.start()

    def load_to_database_thread(self):
        x = threading.Thread(target=self.load_to_database)
        x.start()

    def start_ann_thread(self):
        x = threading.Thread(target=self.start_ann)
        x.start()

    def onUpdateText(self, text):
        cursor = self.textedit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textedit.setTextCursor(cursor)
        self.textedit.ensureCursorVisible()


    def plot(self, graph, color, name):
        self.graphWidget.plot(graph, pen=pyqtgraph.mkPen(color, width=3), name=name)

    def addLegend(self):
        self.graphWidget.addLegend()

    def browse_files(self):
        self.file = QFileDialog.getOpenFileName(self, 'Open file', 'data', 'XLSX (*.xlsx)')
        self.filename.setText(self.file[0].split('/')[-1])
        if self.file is not None:
            self.convert_data_btn.setEnabled(True)

    def load_to_database(self):
        if self.file is None:
            return


        print("Loading and converting data...")
        filename = "data/" + self.filename.text()#.split('/')[-1]
        data_converter = DataConverter(filename)
        ret_data = data_converter.load_and_convert_data()
        print("\nDone.")
        print("\nWriting to database...")
        time1 = time.time()
        data_writer = DataWriter(ret_data)
        data_writer.write_to_database()
        time2 = time.time()
        print("\nDone.")
        print('Writing to database duration: %.2f seconds' % (time2 - time1))

        self.converted_data = ret_data
        if self.converted_data is not None:
            self.start_ann_btn.setEnabled(True)

    def start_ann(self):
        print("\nPreparing data...")
        data_preparer = DataPreparer()
        trainX, trainY, testX, testY = data_preparer.prepare_for_training()
        print("\nDone.")
        print("Doing some learning...")
        ann_regression = AnnRegression()
        time_begin = time.time()
        trainPredict, testPredict = ann_regression.compile_fit_predict(trainX, trainY, testX)
        time_end = time.time()
        print('Training duration: %.2f seconds' % (time_end - time_begin))

        trainPredict, trainY, testPredict, testY = data_preparer.inverse_transform(trainPredict, testPredict)


        print("\nCalculating error...")
        scorer = Scorer()
        trainScore, testScore = scorer.get_score(trainY, trainPredict, testY, testPredict)
        print('Train Score: %.2f RMSE' % (trainScore))
        print('Test Score: %.2f RMSE' % (testScore))
        trainScore, testScore = scorer.get_mape_score(trainY, trainPredict, testY, testPredict)
        print('Train Score: %.2f MAPE' % (trainScore))
        print('Test Score: %.2f MAPE' % (testScore))
        self.plot(testPredict, 'w', "prediction")
        self.plot(testY, 'r', "actual")
        print("\n\n--------------------------------------------------------\n")
        #custom_plotting = Plotting()
        #custom_plotting.show_plots(testPredict, testY)


    def __del__(self):
        sys.stdout = sys.__stdout__