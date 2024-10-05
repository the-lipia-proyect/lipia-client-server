from flask_injector import inject

from utils.responses_helper import ok
from dtos.get_user_configurations_response_dto import GetUserConfigurationsResponseDto
from dtos.update_user_configurations_request_dto import (
    UpdateUserConfigurationsRequestDto,
)
from repositories.user_configurations_repository import UserConfigurationRepository
from repositories.user_repository import UserRepository
from .interfaces.user_configurations_service import IUserConfigurationService


class UserConfigurationService(IUserConfigurationService):
    @inject
    def __init__(
        self,
        user_configuration_repository: UserConfigurationRepository,
        user_repository: UserRepository,
    ):
        self._user_configuration_repository = user_configuration_repository
        self._user_repository = user_repository

    def get_user_configurations_by_user_id(
        self, username: str
    ) -> GetUserConfigurationsResponseDto:
        user = self._user_repository.get_user_by_username(username)
        user_configurations = (
            self._user_configuration_repository.get_user_configurations_by_user_id(
                user["_id"]
            )
        )
        # default values
        user_configurations_values = {
            "frame_delay": 10,
            "selected_camera": "",
            "selected_voice": "",
            "stability": 0.5,
            "similarity_boost": 0.95,
            "style": 0,
            "words_timeout": 3,
            "use_custom_voice": False,
            "facing_mode": "user",
            "playback_rate": 0.5,
            "enable_emergency_phones": False,
            "interpreter_always_active": False,
            "mouth_open_threshold": 20,
        }
        if user_configurations:
            user_configurations_values = {
                "frame_delay": user_configurations.get("frame_delay"),
                "selected_camera": user_configurations.get("selected_camera"),
                "selected_voice": user_configurations.get("selected_voice"),
                "stability": user_configurations.get("stability"),
                "similarity_boost": user_configurations.get("similarity_boost"),
                "style": user_configurations.get("style"),
                "words_timeout": user_configurations.get("words_timeout"),
                "use_custom_voice": user_configurations.get("use_custom_voice"),
                "facing_mode": user_configurations.get("facing_mode"),
                "playback_rate": user_configurations.get("playback_rate", 0.5),
                "enable_emergency_phones": user_configurations.get(
                    "enable_emergency_phones", False
                ),
                "interpreter_always_active": user_configurations.get(
                    "interpreter_always_active", False
                ),
                "mouth_open_threshold": user_configurations.get(
                    "mouth_open_threshold", 20
                ),
            }
        response = GetUserConfigurationsResponseDto(
            frame_delay=user_configurations_values["frame_delay"],
            selected_camera=user_configurations_values["selected_camera"],
            selected_voice=user_configurations_values["selected_voice"],
            stability=user_configurations_values["stability"],
            similarity_boost=user_configurations_values["similarity_boost"],
            style=user_configurations_values["style"],
            words_timeout=user_configurations_values["words_timeout"],
            use_custom_voice=user_configurations_values["use_custom_voice"],
            facing_mode=user_configurations_values["facing_mode"],
            playback_rate=user_configurations_values["playback_rate"],
            enable_emergency_phones=user_configurations_values[
                "enable_emergency_phones"
            ],
            interpreter_always_active=user_configurations_values[
                "interpreter_always_active"
            ],
            mouth_open_threshold=user_configurations_values["mouth_open_threshold"],
        )
        return ok(response)

    def update_user_configuration(
        self, username: str, req: UpdateUserConfigurationsRequestDto
    ):
        user = self._user_repository.get_user_by_username(username)
        user_configurations = (
            self._user_configuration_repository.get_user_configurations_by_user_id(
                user["_id"]
            )
        )
        if user_configurations:
            self._user_configuration_repository.update(user["_id"], req)
        else:
            self._user_configuration_repository.insert(user["_id"], req)
        return ok({})
