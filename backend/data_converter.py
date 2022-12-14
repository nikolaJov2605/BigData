import pandas
import numpy
from database.database import Database
from database.data_manager import DataManager

class DataConverter:
    def __init__(self, filename):
        self.filename = filename


    def load_data(self):
        # ----------------------------- WEATHER COLLECTION ----------------------------- #

        #weather_cols = ["Local time", "T", "Po", "P", "Pa", "U", "DD", "Ff", "N", "WW", "W1", "W2"]
        weather_cols = ["Local time", "T", "Po", "P", "Pa", "U", "Ff"]
        exc_weather = pandas.read_excel(self.filename, sheet_name='weather', usecols=weather_cols)

        exc_weather['Local time'] = pandas.to_datetime(exc_weather['Local time'])
        exc_weather[exc_weather['T']==""] = numpy.NaN
        exc_weather[exc_weather['Po']==""] = numpy.NaN
        exc_weather[exc_weather['P']==""] = numpy.NaN
        exc_weather[exc_weather['Pa']==""] = numpy.NaN
        exc_weather[exc_weather['U']==""] = numpy.NaN
        exc_weather[exc_weather['Ff']==""] = numpy.NaN
        #exc_weather.fillna(method='ffill', inplace=True)

        interpolation_collumns = ["T", "Po", "P", "Pa", "U", "Ff"]
        exc_weather[interpolation_collumns] = exc_weather[interpolation_collumns].astype(float).apply(lambda x: x.interpolate(method='linear'))
        

        weather_data = exc_weather


        # ----------------------------- LOAD COLLECTION ----------------------------- #

        load_cols = ["DateShort", "TimeFrom", "TimeTo", "Load (MW/h)"]
        exc_load = pandas.read_excel(self.filename, sheet_name='load', usecols=load_cols)
        exc_load["DateShort"] = exc_load['DateShort'].astype(str) + " " + exc_load["TimeFrom"].astype(str)
        exc_load['DateShort'] = pandas.to_datetime(exc_load['DateShort'])
        del exc_load['TimeFrom']
        del exc_load['TimeTo']
        exc_load.rename(columns={'Load (MW/h)':'load'}, inplace=True)
        exc_load.rename(columns={'DateShort':'Local time'}, inplace=True)

        load_data = exc_load



        # --------------------------- MEARGED COLLECTIONS --------------------------- #

        measures = pandas.merge(exc_weather, exc_load, on='Local time', how='inner')
        #df['date'] = pd.to_datetime(df['date'])    
        #df['date_delta'] = (df['date'] - df['date'].min())  / np.timedelta64(1,'D')
        measures['Local time'] = pandas.to_datetime(measures['Local time'])
        measures['Local time'] = (measures['Local time'] - measures['Local time'].min())  / numpy.timedelta64(1,'D')

        measures.to_csv('measures.csv', index=False)

        return measures
        
        # --------------------------------------------------------------------------- #


        
