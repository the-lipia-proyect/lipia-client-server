from typing import Dict, Any
from bson import ObjectId
import datetime
from time import time

from pymongo.collection import Collection
from services.mongodb_service import MongoDBClient
from flask_injector import inject

from dtos.sign_up_request_dto import SignUpRequestDto
from utils.date_helper import get_utc_timestamp


class UserRepository:
    @inject
    def __init__(self, mongodb_client: MongoDBClient):
        self._users_collection: Collection = mongodb_client.get_database()["Users"]

    def get_all_users(self):
        return list(self._users_collection.find())

    def get_user_by_id(self, id: str) -> Dict[str, Any]:
        return self._users_collection.find_one({"_id": ObjectId(id)})

    def get_user_by_username(self, username: str) -> Dict[str, Any]:
        return self._users_collection.find_one({"username": username})

    def get_user_by_email(self, email: str):
        return self._users_collection.find_one({"email": email})

    def insert(self, user_id: str, user_dto: SignUpRequestDto):
        new_user = {
            "_id": user_id,
            "email": str(user_dto.email),
            "name": user_dto.name,
            "surname": user_dto.surname,
            "phone_number": user_dto.phone_number,
            "username": user_dto.username,
            "created_at": get_utc_timestamp(),
            "updated_at": get_utc_timestamp(),
        }
        insert_result = self._users_collection.insert_one(new_user)
        return insert_result.inserted_id

    def update(self, user_id: str, update_fields: Dict[str, Any]):
        return
