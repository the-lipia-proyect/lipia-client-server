from flask_injector import inject

from dtos.generate_audio_file_request_dto import (
    GenerateAudioFileRequestDto,
    VoiceSettingsDto,
)
from utils.responses_helper import ok, not_found
from dtos.get_user_shortcuts_response_dto import GetUserShortcutsResponseDto, Shortcut
from dtos.generate_shortcut_request_dto import GenerateShortcutRequestDto
from dtos.generate_shortcut_response_dto import GenerateShortcutResponseDto
from dtos.update_shortcut_request_dto import UpdateShortcutRequestDto
from repositories.shortcuts_repository import ShortcutRepository
from repositories.user_configurations_repository import UserConfigurationRepository
from .interfaces.shortcuts_service import IShortcutsService
from .interfaces.voices_service import IVoicesService
from database.collection_models.shortcut_model import Shortcut as ShortCutModel


class ShortcutsService(IShortcutsService):
    @inject
    def __init__(
        self,
        shortcuts_repository: ShortcutRepository,
        user_configuration_repositroy: UserConfigurationRepository,
        voices_service: IVoicesService,
    ):
        self._shortcuts_repository = shortcuts_repository
        self._user_configuration_repository = user_configuration_repositroy
        self._voices_service = voices_service

    def get_user_shortcuts(
        self, user_id: str, order_by: str, descending_order: bool
    ) -> GetUserShortcutsResponseDto:
        shortcuts_list = self._shortcuts_repository.get_by_user_id(
            user_id, order_by, descending_order
        )
        shortcuts = [
            Shortcut(
                id=str(data.get("_id")),
                text=data.get("text"),
                image_url=data.get("image_url"),
                order=data.get("order"),
                audio_file_url=data.get("audio_file_url"),
            )
            for data in shortcuts_list
        ]
        response = GetUserShortcutsResponseDto(shortcuts=shortcuts).model_dump()
        return ok(response)

    def insert_user_shortcut(self, user_id: str, req: GenerateShortcutRequestDto):
        shortcut = ShortCutModel(
            image=req.image,
            text=req.text,
            user_id=user_id,
            order=req.order,
        )
        user_configuration = (
            self._user_configuration_repository.get_user_configurations_by_user_id(
                user_id
            )
        )
        if user_configuration:
            generate_audio_result = self._voices_service.generate_audio_file(
                GenerateAudioFileRequestDto(
                    text=req.text,
                    voice_id=user_configuration.get("selected_voice"),
                    voice_settings=VoiceSettingsDto(
                        stability=user_configuration.get("stability"),
                        similarity_boost=user_configuration.get("similarity_boost"),
                        style=user_configuration.get("style"),
                    ),
                )
            )
            generate_audio_json_result = generate_audio_result[0].get_json()
            shortcut.audio_file_url = generate_audio_json_result.get("file_url")

        db_user_id = self._shortcuts_repository.insert(shortcut)
        response = GenerateShortcutResponseDto(id=db_user_id).model_dump()
        return ok(response)

    def update_user_shortcut(
        self, id: str, user_id: str, req: UpdateShortcutRequestDto
    ):
        shortcut = self._shortcuts_repository.get_by_id(id)
        if not shortcut:
            return not_found({"message": "The shortcut does not exist"})

        shortcut = ShortCutModel(
            image=req.image,
            text=req.text,
            user_id=user_id,
            order=req.order,
            audio_file_url=None,
        )

        user_configuration = (
            self._user_configuration_repository.get_user_configurations_by_user_id(
                user_id
            )
        )
        if user_configuration:
            generate_audio_result = self._voices_service.generate_audio_file(
                GenerateAudioFileRequestDto(
                    text=req.text,
                    voice_id=user_configuration.get("selected_voice"),
                    voice_settings=VoiceSettingsDto(
                        stability=user_configuration.get("stability"),
                        similarity_boost=user_configuration.get("similarity_boost"),
                        style=user_configuration.get("style"),
                    ),
                )
            )
            generate_audio_json_result = generate_audio_result[0].get_json()
            shortcut.audio_file_url = generate_audio_json_result.get("file_url")

        self._shortcuts_repository.update(id, shortcut)
        return ok({})

    def delete_user_shortcut(self, id: str):
        shortcut = self._shortcuts_repository.get_by_id(id)
        if not shortcut:
            return not_found({"message": "The shortcut does not exist"})
        self._shortcuts_repository.delete(id)
        return ok({})
