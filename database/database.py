from pymongo import MongoClient

class Database:
    def __init__(self):
        self.connectionString = "mongodb://localhost:27017"
        self.client = MongoClient(self.connectionString)

    def get_client(self):
        return self.client

    def get_database_names(self):
        return self.client.list_database_names()

    def get_bigdata_db_context(self):
        context = self.client.BigDataDB
        return context

