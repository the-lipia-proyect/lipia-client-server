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
            "frame_delay": 50,
            "selected_camera": "",
            "selected_voice": "",
            "stability": 0.5,
            "similarity_boost": 0.95,
            "style": 0,
        }
        if user_configurations:
            user_configurations_values = {
                "frame_delay": user_configurations.get("frame_delay"),
                "selected_camera": user_configurations.get("selected_camera"),
                "selected_voice": user_configurations.get("selected_voice"),
                "stability": user_configurations.get("stability"),
                "similarity_boost": user_configurations.get("similarity_boost"),
                "style": user_configurations.get("style"),
            }

        response = GetUserConfigurationsResponseDto(
            frame_delay=user_configurations_values["frame_delay"],
            selected_camera=user_configurations_values["selected_camera"],
            selected_voice=user_configurations_values["selected_voice"],
            stability=user_configurations_values["stability"],
            similarity_boost=user_configurations_values["similarity_boost"],
            style=user_configurations_values["style"],
        ).model_dump()
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
