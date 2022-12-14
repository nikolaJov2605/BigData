from database.database import Database

class DataManager:
    def __init__(self):
        self.database = Database()
        self.db_context = self.database.get_bigdata_db_context()
        self.measure_data = self.db_context.measures

    def measure_data_collection_count(self):
        return self.measure_data.count_documents({})


    def write_measure_data(self, data):
        try:
            result = self.measure_data.insert_many(data, ordered=True)
        except:
            result = None
            return result

        return result
        

    def delete_measure_data(self):
        try:
            result = self.measure_data.delete_many({})
        except:
            result = None
            return result
        
        return result

    def get_measure_data(self):
        try:
            result = self.measure_data.find({})
        except:
            result = None
            return result
        return result
    


