from database.database import Database

class DataManager:
    def __init__(self):
        self.database = Database()
        self.db_context = self.database.get_bigdata_db_context()
        self.weather_data = self.db_context.weather
        self.load_data = self.db_context.load

    def weather_collection_count(self):
        return self.weather_data.count_documents({})
        
    def load_collection_count(self):
        return self.load_data.count_documents({})

    def write_weather_data(self, data):
        try:
            result = self.weather_data.insert_many(data, ordered=True)
        except:
            result = None
            return result

        return result

    def write_load_data(self, data):
        try:
            result = self.load_data.insert_many(data, ordered=True)
        except:
            result = None
            return result
        
        return result

    def delete_weather_data(self):
        try:
            result = self.weather_data.delete_many({})
        except:
            result = None
            return result
        
        return result

    def delete_load_data(self):
        try:
            result = self.load_data.delete_many({})
        except:
            result = None
            return result
        return result
