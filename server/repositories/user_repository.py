from typing import Dict, Any
from bson import ObjectId

from pymongo.collection import Collection
from services.mongodb_service import MongoDBClient
from flask_injector import inject

from dtos.sign_up_request_dto import SignUpRequestDto
from dtos.update_user_profile_request_dto import UpdateUserProfileRequestDto
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

    def insert(self, user_id: str, user_dto: SignUpRequestDto) -> str:
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

    def update(self, user_id: str, update_user_dto: UpdateUserProfileRequestDto):
        try:
            update_user_fields = {
                "name": update_user_dto.name,
                "surname": update_user_dto.surname,
                "updated_at": get_utc_timestamp(),
                "phone_number_emergency": update_user_dto.phone_number_emergency,
                "phone_number_doctor": update_user_dto.phone_number_doctor,
                "phone_number_doctor_emergency": update_user_dto.phone_number_doctor_emergency,
                "blood_type": update_user_dto.blood_type,
            }
            if update_user_dto.phone_number:
                update_user_fields["phone_number"] = update_user_dto.phone_number
            result = self._users_collection.update_one(
                {"_id": user_id}, {"$set": update_user_fields}
            )
        except Exception as e:
            print("ERROR", e)
            raise e
