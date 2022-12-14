from database.data_manager import DataManager


class DataWriter:
    def __init__(self, measures):
        self.measure_file_data = measures
        self.data_manager = DataManager()

    def write_to_database(self):
        if self.data_manager.measure_data_collection_count() == 0:
            result = self.data_manager.write_measure_data(self.measure_file_data.to_dict('records'))
            if result == None:
                print("Error ocured while writing to measure_data_collection")
        else:
            if self.data_manager.measure_data_collection_count() != len(self.measure_file_data.index):
                result = self.data_manager.delete_measure_data()
                if result == None:
                    print("Error ocured while removing from measure_data_collection")
                result = self.data_manager.write_measure_data(self.measure_file_data.to_dict('records'))