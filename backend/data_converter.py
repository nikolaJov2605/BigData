import pandas
import numpy
from database.database import Database

class DataConverter:
    def __init__(self, filename):
        self.filename = filename


    def load_data(self):
        # ----------------------------- WEATHER COLLECTION ----------------------------- #

        #weather_cols = ["Local time", "T", "Po", "P", "Pa", "U", "DD", "Ff", "N", "WW", "W1", "W2"]
        weather_cols = ["Local time", "T", "Po", "P", "Pa", "U", "Ff"]
        exc_weather = pandas.read_excel(self.filename, sheet_name='weather', usecols=weather_cols)

        exc_weather['Local time'] = pandas.to_datetime(exc_weather['Local time'])
        exc_weather[exc_weather['Pa']==""] = numpy.NaN
        exc_weather[exc_weather['U']==""] = numpy.NaN
        exc_weather[exc_weather['Ff']==""] = numpy.NaN
        exc_weather.fillna(method='ffill', inplace=True)

        weather_data = exc_weather


        # ----------------------------- LOAD COLLECTION ----------------------------- #

        load_cols = ["DateShort", "TimeFrom", "TimeTo", "Load (MW/h)"]
        exc_load = pandas.read_excel(self.filename, sheet_name='load', usecols=load_cols)
        exc_load["DateShort"] = exc_load['DateShort'].astype(str) + " " + exc_load["TimeFrom"].astype(str)
        exc_load['DateShort'] = pandas.to_datetime(exc_load['DateShort'])
        del exc_load['TimeFrom']
        del exc_load['TimeTo']
        #exc_load[exc_load['Load (MW/h)']==""] = numpy.NaN
        #exc_load.fillna(method='ffill', inplace=True)

        load_data = exc_load


        return [weather_data, load_data]
        
        # ----------------------------- DATABASE ----------------------------- #

        database = Database()

        context = database.get_bigdata_db_context()

        weather_set = context.weather
        load_set = context.load

        

        try:
            if weather_set.count_documents({}) == 0:
                result = weather_set.insert_many(exc_weather.to_dict('records'), ordered=True)
            else:
                if weather_set.count_documents({}) != len(exc_weather.index):
                    weather_set.delete_many({})
                    result = weather_set.insert_many(exc_weather.to_dict('records'), ordered=True)
        except:
            print("Error ocured while writing to database (WEATHER)")

        try:
            if load_set.count_documents({}) == 0:
                result = load_set.insert_many(exc_load.to_dict('records'), ordered=True)
            else:
                if load_set.count_documents({}) != len(exc_load.index):
                    load_set.delete_many({})
                    result = load_set.insert_many(exc_load.to_dict('records'), ordered=True)
        except:
            print("Error ocured while writing to database (LOAD)")

        
        print("WEATHER SET: ", weather_set.count_documents({}))
        print("LOAD SET: ", load_set.count_documents({}))
        print("WEATHER EXCEL: ", len(exc_weather.index))
        print("LOAD EXCEL: ", len(exc_load.index))
        exc_weather.to_csv("weather.csv", index = None, header = True)
        exc_load.to_csv("load.csv", index=None, header=True)

    def write_data(self):
        database = Database()
        print(database.client)
        print(database.connectionString)
        db = database.get_bigdata_db_context()
        weather = db.weather
       # result = weather.insert_one() # upis
        
