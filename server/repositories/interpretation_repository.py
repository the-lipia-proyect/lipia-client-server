from typing import Dict, Any
from bson import ObjectId

from pymongo.collection import Collection
from services.mongodb_service import MongoDBClient
from flask_injector import inject

from utils.date_helper import get_utc_timestamp
from database.collection_models.interpretation_model import Interpretation


class InterpretationRepository:
    @inject
    def __init__(self, mongodb_client: MongoDBClient):
        self._interpretations_collection: Collection = mongodb_client.get_database()[
            "Interpretations"
        ]

    def get_by_id(self, id: str) -> Dict[str, Any] | None:
        return self._interpretations_collection.find_one({"_id": ObjectId(id)})

    def get_by_user_id(
        self, user_id: str, order_by: str, descending_order: str
    ) -> list[Dict[str, Any]] | None:
        sort_order = -1 if descending_order else 1
        cursor = self._interpretations_collection.find({"user_id": user_id}).sort(
            order_by, sort_order
        )
        return list(cursor)

    def insert(self, interpretation: Interpretation) -> str:
        interpretation = {
            "words": [
                {"prediction": word.prediction, "data": word.data}
                for word in interpretation.words
            ],
            "user_id": interpretation.user_id,
            "created_at": get_utc_timestamp(),
            "updated_at": get_utc_timestamp(),
            "note": None,
        }
        insert_result = self._interpretations_collection.insert_one(interpretation)
        return str(insert_result.inserted_id)

    def update(
        self,
        id: str,
        interpretation: Interpretation,
    ):
        try:
            update_interpretation_fields = {
                "words": [
                    {"prediction": word.prediction, "data": word.data}
                    for word in interpretation.words
                ],
                "user_id": interpretation.user_id,
                "note": interpretation.note,
                "updated_at": get_utc_timestamp(),
            }
            result = self._interpretations_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": update_interpretation_fields}
            )
        except Exception as e:
            print("ERROR", e)
            raise e
