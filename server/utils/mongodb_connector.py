import os

import pymongo

DB_NAME = "lipia_database"
DB_USERNAME = os.getenv("MONGODB_USERNAME")
DB_PASSWORD = os.getenv("MONGODB_PASSWORD")
DB_CLUSTER = os.getenv("MONGODB_CLUSTER")
CONNECTION_STRING = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_CLUSTER}/"
mongodb_client = pymongo.MongoClient(CONNECTION_STRING)

db = mongodb_client[DB_NAME]
