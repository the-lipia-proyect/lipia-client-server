from typing import Dict, Any

from pymongo.collection import Collection
from services.mongodb_service import MongoDBClient
from flask_injector import inject

from dtos.update_user_configurations_request_dto import (
    UpdateUserConfigurationsRequestDto,
)
from utils.date_helper import get_utc_timestamp


class UserConfigurationRepository:
    @inject
    def __init__(self, mongodb_client: MongoDBClient):
        self._users_configurations_collection: Collection = (
            mongodb_client.get_database()["UserConfigurations"]
        )

    def get_user_configurations_by_user_id(
        self, user_configuration_id: str
    ) -> Dict[str, Any] | None:
        return self._users_configurations_collection.find_one(
            {"_id": user_configuration_id}
        )

    def insert(
        self, user_id: str, user_configuration_dto: UpdateUserConfigurationsRequestDto
    ) -> str:
        new_user_configuration = {
            "_id": user_id,
            "frame_delay": user_configuration_dto.frame_delay,
            "selected_voice": user_configuration_dto.selected_voice,
            "selected_camera": user_configuration_dto.selected_camera,
            "stability": user_configuration_dto.stability,
            "similarity_boost": user_configuration_dto.similarity_boost,
            "style": user_configuration_dto.style,
            "words_timeout": user_configuration_dto.words_timeout,
            "use_custom_voice": user_configuration_dto.use_custom_voice,
            "facing_mode": user_configuration_dto.facing_mode,
            "playback_rate": user_configuration_dto.playback_rate,
            "enable_emergency_phones": user_configuration_dto.enable_emergency_phones,
            "created_at": get_utc_timestamp(),
            "updated_at": get_utc_timestamp(),
            "interpreter_always_active": user_configuration_dto.interpreter_always_active,
            "mouth_open_threshold": user_configuration_dto.mouth_open_threshold,
            "interpreter_compress_frames": user_configuration_dto.interpreter_compress_frames,
            "use_lipnet_model": user_configuration_dto.use_lipnet_model,
        }
        insert_result = self._users_configurations_collection.insert_one(
            new_user_configuration
        )
        return insert_result.inserted_id

    def update(
        self,
        id: str,
        update_user_configuration_dto: UpdateUserConfigurationsRequestDto,
    ):
        try:
            update_user_configurations_fields = {
                "frame_delay": update_user_configuration_dto.frame_delay,
                "selected_voice": update_user_configuration_dto.selected_voice,
                "selected_camera": update_user_configuration_dto.selected_camera,
                "stability": update_user_configuration_dto.stability,
                "similarity_boost": update_user_configuration_dto.similarity_boost,
                "style": update_user_configuration_dto.style,
                "words_timeout": update_user_configuration_dto.words_timeout,
                "use_custom_voice": update_user_configuration_dto.use_custom_voice,
                "facing_mode": update_user_configuration_dto.facing_mode,
                "playback_rate": update_user_configuration_dto.playback_rate,
                "enable_emergency_phones": update_user_configuration_dto.enable_emergency_phones,
                "updated_at": get_utc_timestamp(),
                "interpreter_always_active": update_user_configuration_dto.interpreter_always_active,
                "mouth_open_threshold": update_user_configuration_dto.mouth_open_threshold,
                "interpreter_compress_frames": update_user_configuration_dto.interpreter_compress_frames,
                "use_lipnet_model": update_user_configuration_dto.use_lipnet_model,
            }
            result = self._users_configurations_collection.update_one(
                {"_id": id}, {"$set": update_user_configurations_fields}
            )
        except Exception as e:
            print("ERROR", e)
            raise e
