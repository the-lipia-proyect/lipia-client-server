from typing import Dict, Any, Optional
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
        self,
        user_id: str,
        order_by: str,
        descending_order: str,
        page: Optional[int] = 1,
        page_size: Optional[int] = None,
        from_date: Optional[int] = None,
    ) -> list[Dict[str, Any]] | None:
        sort_order = -1 if descending_order else 1
        query_filter = {"user_id": user_id}

        if from_date is not None:
            query_filter["created_at"] = {"$gt": from_date}

        cursor = self._interpretations_collection.find(query_filter).sort(
            order_by, sort_order
        )

        if page_size is not None:
            skip_count = (page - 1) * page_size
            cursor = cursor.skip(skip_count).limit(page_size)

        return list(cursor)

    def insert(self, interpretation: Interpretation) -> str:
        interpretation = {
            "word": {
                "prediction": interpretation.word.prediction,
                "order": interpretation.word.order,
            },
            "phrase_group": interpretation.phrase_group,
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
                "phrase_group": interpretation.phrase_group,
                "user_id": interpretation.user_id,
                "note": interpretation.note,
                "updated_at": get_utc_timestamp(),
            }
            if interpretation.word:
                update_interpretation_fields["word"] = {
                    "prediction": interpretation.word.prediction,
                    "order": interpretation.word.order,
                }
            result = self._interpretations_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": update_interpretation_fields}
            )
        except Exception as e:
            print("ERROR", e)
            raise e
