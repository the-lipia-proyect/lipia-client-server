from typing import Dict, Any

from pymongo.collection import Collection
from services.mongodb_service import MongoDBClient
from flask_injector import inject

from utils.date_helper import get_utc_timestamp
from database.collection_models.interpretation_detail_model import InterpretationDetail


class InterpretationDetailsRepository:
    @inject
    def __init__(self, mongodb_client: MongoDBClient):
        self._interpretation_details_collection: Collection = (
            mongodb_client.get_database()["InterpretationDetails"]
        )

    def get_by_id(self, id: str) -> Dict[str, Any] | None:
        return self._interpretation_details_collection.find_one({"_id": id})

    def insert(self, interpretation_detail: InterpretationDetail) -> str:
        interpretation = {
            "_id": interpretation_detail.id,
            "frames": interpretation_detail.frames,
            "created_at": get_utc_timestamp(),
            "updated_at": get_utc_timestamp(),
        }
        insert_result = self._interpretation_details_collection.insert_one(
            interpretation
        )
        return str(insert_result.inserted_id)
