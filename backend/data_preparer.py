import numpy
import pandas
from database.data_manager import DataManager
from sklearn.preprocessing import MinMaxScaler

SHARE_FOR_TRAINING = 0.85

class DataPreparer:
    def __init__(self):
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        dataframe = self.load_data_from_database()
        #self.datasetOrig = self.datasetOrig.astype('float32')
        self.number_of_columns = len(dataframe.columns)
        self.datasetOrig = dataframe.values
        self.datasetOrig = self.datasetOrig.astype('float32')
        self.predictor_column_no = self.number_of_columns - 1
        self.share_for_training = SHARE_FOR_TRAINING

    def load_data_from_database(self):
        data_manager = DataManager()
        data = data_manager.get_measure_data()
        data_list = list(data)
        dataframe = pandas.DataFrame(data_list)
        del dataframe['_id']
        #del dataframe['Local time']
        return dataframe

    
    def prepare_for_training(self):
        dataset = self.scaler.fit_transform(self.datasetOrig)                       #skaliranje
        print(dataset.max(axis=0)) # will return max value of each column
        print(dataset.min(axis=0))
        train_size = int(len(dataset) * self.share_for_training)                    #velicina podataka za trening
        test_size = len(dataset) - train_size                                       #velicina za test
        train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]   # definicija setova za trening i test
        print(len(train), len(test))        
        look_back = self.number_of_columns
        trainX, trainY = self.create_dataset(train, look_back)              # podela na zavisne i nezavisne podatke
        testX, testY = self.create_dataset(test, look_back)
        trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))   # skaliranje
        testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))       # skaliranje
        self.trainX = trainX
        self.trainY = trainY
        self.testX = testX
        self.testY = testY
        return trainX.copy(), trainY.copy(), testX.copy(), testY.copy()

    def inverse_transform(self, trainPredict, testPredict): # vracanje na prave vrednosti
        trainPredict = numpy.reshape(trainPredict, (trainPredict.shape[0], trainPredict.shape[1]))
        testPredict = numpy.reshape(testPredict, (testPredict.shape[0], testPredict.shape[1]))
        self.trainX = numpy.reshape(self.trainX, (self.trainX.shape[0], self.trainX.shape[2]))
        self.testX = numpy.reshape(self.testX, (self.testX.shape[0], self.testX.shape[2]))
        trainXAndPredict = numpy.concatenate((self.trainX, trainPredict),axis=1)
        testXAndPredict = numpy.concatenate((self.testX, testPredict),axis=1)
        trainY = numpy.reshape(self.trainY, (self.trainY.shape[0], 1))
        testY = numpy.reshape(self.testY, (self.testY.shape[0], 1))
        trainXAndY = numpy.concatenate((self.trainX, trainY),axis=1)
        testXAndY = numpy.concatenate((self.testX, testY),axis=1)
        trainXAndPredict = self.scaler.inverse_transform(trainXAndPredict)
        trainXAndY = self.scaler.inverse_transform(trainXAndY)
        testXAndPredict = self.scaler.inverse_transform(testXAndPredict)
        testXAndY = self.scaler.inverse_transform(testXAndY)
        trainPredict = trainXAndPredict[:,self.predictor_column_no];
        trainY = trainXAndY[:,self.predictor_column_no]
        testPredict = testXAndPredict[:,self.predictor_column_no];
        testY = testXAndY[:,self.predictor_column_no];
        return trainPredict, trainY, testPredict, testY


    def create_dataset(self, dataset, look_back):
        dataX, dataY = [], []
        for i in range(len(dataset)-1):
            a = dataset[i, 0:look_back-1]
            dataX.append(a)
            dataY.append(dataset[i, look_back-1])
        return numpy.array(dataX), numpy.array(dataY)
