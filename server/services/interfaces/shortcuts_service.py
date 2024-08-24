from abc import ABC, abstractmethod
from dtos.update_shortcut_request_dto import (
    UpdateShortcutRequestDto,
)
from dtos.generate_shortcut_request_dto import (
    GenerateShortcutRequestDto,
)
from dtos.get_user_shortcuts_response_dto import GetUserShortcutsResponseDto


class IShortcutsService(ABC):
    @abstractmethod
    def get_user_shortcuts(
        self, user_id: str, order_by: str, descending_order: bool
    ) -> GetUserShortcutsResponseDto:
        pass

    @abstractmethod
    def insert_user_shortcut(self, user_id: str, req: GenerateShortcutRequestDto):
        pass

    @abstractmethod
    def update_user_shortcut(
        self, id: str, user_id: str, req: UpdateShortcutRequestDto
    ):
        pass

    @abstractmethod
    def delete_user_shortcut(self, id: str):
        pass
