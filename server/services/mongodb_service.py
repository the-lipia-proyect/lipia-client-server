import pymongo
from pymongo.database import Database


class MongoDBClient:
    def __init__(
        self, db_name: str, db_username: str, db_password: str, db_cluster: str
    ):
        connection_string = f"mongodb+srv://{db_username}:{db_password}@{db_cluster}/"
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[db_name]

    def get_database(self) -> Database:
        return self.db
