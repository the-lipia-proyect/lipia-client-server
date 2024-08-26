from typing import Dict, Any

from bson import ObjectId
from pymongo.collection import Collection
from services.mongodb_service import MongoDBClient
from flask_injector import inject

from database.collection_models.shortcut_model import Shortcut
from utils.date_helper import get_utc_timestamp


class ShortcutRepository:
    @inject
    def __init__(self, mongodb_client: MongoDBClient):
        self._shortcuts_collection: Collection = mongodb_client.get_database()[
            "Shortcuts"
        ]

    def get_by_id(self, id: str) -> Dict[str, Any] | None:
        return self._shortcuts_collection.find_one({"_id": ObjectId(id)})

    def get_by_user_id(
        self, user_id: str, order_by: str, descending_order: str
    ) -> list[Dict[str, Any]] | None:
        sort_order = -1 if descending_order else 1

        cursor = self._shortcuts_collection.find({"user_id": user_id}).sort(
            order_by, sort_order
        )
        return list(cursor)

    def insert(self, shortcut: Shortcut) -> str:
        new_shortcut = {
            "text": shortcut.text,
            "image_url": shortcut.image,
            "user_id": shortcut.user_id,
            "order": shortcut.order,
            "audio_file_url": shortcut.audio_file_url,
            "voice_description": shortcut.voice_description,
            "created_at": get_utc_timestamp(),
            "updated_at": get_utc_timestamp(),
        }
        insert_result = self._shortcuts_collection.insert_one(new_shortcut)
        return str(insert_result.inserted_id)

    def update(
        self,
        id: str,
        shortcut: Shortcut,
    ):
        try:
            update_user_shortcut_fields = {
                "text": shortcut.text,
                "image_url": shortcut.image,
                "user_id": shortcut.user_id,
                "order": shortcut.order,
                "audio_file_url": shortcut.audio_file_url,
                "voice_description": shortcut.voice_description,
                "updated_at": get_utc_timestamp(),
            }
            result = self._shortcuts_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": update_user_shortcut_fields}
            )
        except Exception as e:
            print("ERROR", e)
            raise e

    def delete(self, id: str) -> bool:
        try:
            result = self._shortcuts_collection.delete_one({"_id": ObjectId(id)})
            if result.deleted_count == 0:
                return False
            return True
        except Exception as e:
            print("ERROR", e)
            raise e
