from database.data_manager import DataManager


class DataWriter:
    def __init__(self, data_tuple):
        self.weather_file_data = data_tuple[0]
        self.load_file_data = data_tuple[1]
        self.data_manager = DataManager()

    def write_to_database(self):
        if self.data_manager.weather_collection_count() == 0:
            result = self.data_manager.write_weather_data(self.weather_file_data.to_dict('records'))
            if result == None:
                print("Error ocured while writing to weather_collection")
        else:
            if self.data_manager.weather_collection_count() != len(self.weather_file_data.index):
                result = self.data_manager.delete_weather_data()
                if result == None:
                    print("Error ocured while removing from weather_collection")
                result = self.data_manager.write_weather_data(self.weather_file_data.to_dict('records'))

        if self.data_manager.load_collection_count() == 0:
            result = self.data_manager.write_load_data(self.load_file_data.to_dict('records'))
            if result == None:
                print("Error ocured while writing to load_collection")
        else:
            if self.data_manager.load_collection_count() != len(self.load_file_data.index):
                result = self.data_manager.delete_load_data()
                if result == None:
                    print("Error ocured while removing from load_collection")
                result = self.data_manager.write_load_data(self.load_file_data.to_dict('records'))