from typing import Dict, Any, Optional

from pymongo.collection import Collection
from services.mongodb_service import MongoDBClient
from flask_injector import inject

from utils.date_helper import get_utc_timestamp


class UserVoiceRepository:
    @inject
    def __init__(self, mongodb_client: MongoDBClient):
        self._users_voices_collection: Collection = mongodb_client.get_database()[
            "UserVoices"
        ]

    def get_user_voice_by_user_id_and_id(
        self, user_id: str, id: str
    ) -> Optional[Dict[str, Any]]:
        return self._users_voices_collection.find_one({"user_id": user_id, "_id": id})

    def insert(self, user_id: str, voice_id: str) -> str:
        new_user_voice = {
            "_id": voice_id,
            "user_id": user_id,
            "created_at": get_utc_timestamp(),
            "updated_at": get_utc_timestamp(),
        }
        insert_result = self._users_voices_collection.insert_one(new_user_voice)
        return insert_result.inserted_id

    def delete(self, id: str) -> bool:
        try:
            result = self._users_voices_collection.delete_one({"_id": id})
            if result.deleted_count == 0:
                return False
            return True
        except Exception as e:
            print("ERROR", e)
            raise e
