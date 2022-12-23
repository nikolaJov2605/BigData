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
        weather_cols = ["Local time", "T", "Po", "P", "Pa", "U", "Ff", "N"]
        exc_weather = pandas.read_excel(self.filename, sheet_name='weather', usecols=weather_cols)

        exc_weather['Local time'] = pandas.to_datetime(exc_weather['Local time'], dayfirst=True)

        exc_weather[exc_weather['T']==""] = numpy.NaN
        exc_weather[exc_weather['Po']==""] = numpy.NaN
        exc_weather[exc_weather['P']==""] = numpy.NaN
        exc_weather[exc_weather['Pa']==""] = numpy.NaN
        exc_weather[exc_weather['U']==""] = numpy.NaN
        exc_weather[exc_weather['Ff']==""] = numpy.NaN
        exc_weather[exc_weather['N']==""] = numpy.NaN
        #exc_weather.fillna(method='ffill', inplace=True)
        exc_weather['N'].fillna(method='ffill', inplace=True)
        exc_weather['N'].fillna(method='bfill', inplace=True)

        exc_weather['N'] = numpy.where(exc_weather['N'].str.contains('–'), exc_weather['N'].str.replace('–', ' ', regex=False) , exc_weather['N'])
        exc_weather["N"] = exc_weather['N'].str.split(pat=' ', n=-1, expand=True)[0]
        exc_weather['N'] = numpy.where(exc_weather['N']=='no', '0', exc_weather['N'])
        exc_weather['N'] = numpy.where(exc_weather['N'].str.contains('%'), exc_weather['N'].str.replace('%', '', regex=False) , exc_weather['N'])
        exc_weather['N'] = numpy.where(exc_weather['N'].str.contains('.'), exc_weather['N'].str.replace('.', '', regex=False) , exc_weather['N'])
        exc_weather['N'] = numpy.where(exc_weather['N'].str.contains('Sky'), exc_weather['N'].str.replace('Sky', '100', regex=False) , exc_weather['N'])
        exc_weather['N'] = exc_weather['N'].astype('float') / 100
        #exc_weather['N'] = exc_weather['N'].str.split(pat='%', n=-1, expand=True)[0]
        #exc_weather[exc_weather['N'].str.contains("–")] = exc_weather['N'].str.split(pat='–', n=-1, expand=True)[0]

        

        interpolation_collumns = ["T", "Po", "P", "Pa", "U", "Ff", "N"]
        exc_weather[interpolation_collumns] = exc_weather[interpolation_collumns].astype(float).apply(lambda x: x.interpolate(method='linear'))

        #exc_weather['last_day_average_temperature']

        exc_weather.to_csv('weather.csv', index=False)


        # ----------------------------- LOAD COLLECTION ----------------------------- #

        load_cols = ["DateShort", "TimeFrom", "TimeTo", "Load (MW/h)"]
        exc_load = pandas.read_excel(self.filename, sheet_name='load', usecols=load_cols)
        exc_load["DateShort"] = exc_load['DateShort'].astype(str) + " " + exc_load["TimeFrom"].astype(str)
        exc_load['DateShort'] = pandas.to_datetime(exc_load['DateShort'], yearfirst=True)
        del exc_load['TimeFrom']
        del exc_load['TimeTo']
        exc_load.rename(columns={'Load (MW/h)':'load'}, inplace=True)
        exc_load.rename(columns={'DateShort':'Local time'}, inplace=True)


        #exc_load.to_csv('load.csv', index=False)



        # --------------------------- MEARGED COLLECTIONS --------------------------- #

        measures = pandas.merge(exc_weather, exc_load, on='Local time', how='left')
        date = pandas.DataFrame()
        date['dayType'] = measures['Local time'].dt.day % 7
        date['month'] = measures['Local time'].dt.month
    #    date['date'] = measures['Local time'].dt.date
        ###measures['dayType'] = date['dayType']
        #df.insert(0, 'mean', df.pop('mean'))
        measures.insert(0, 'dayType', date['dayType'])
        measures.insert(1, 'month', date['month'])
        #measures.insert(1, 'date', date['date'])






        # NAPRAVI NOVI DATAFRAME GRUPA SA DATUMIMA I PROSECNOM POTROSNJOM I URADI MERGE
        #date['date'] = measures.groupby(['date'])
        #date['averageLastDayConsumption'] = measures.groupby(['date'])['load'].mean()


        #measures['averageLastDayConsumption'] = loads




        #measures.insert(2, 'averageLastDayConsumption', date['averageLastDayConsumption'])
        del measures['Local time']


        measures.to_csv('measures.csv', index=False)

        return measures

        # --------------------------------------------------------------------------- #

