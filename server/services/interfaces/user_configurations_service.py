from abc import ABC, abstractmethod
from dtos.update_user_configurations_request_dto import (
    UpdateUserConfigurationsRequestDto,
)
from dtos.get_user_configurations_response_dto import GetUserConfigurationsResponseDto


class IUserConfigurationService(ABC):
    @abstractmethod
    def get_user_configurations_by_user_id(
        self, username: str
    ) -> GetUserConfigurationsResponseDto:
        pass

    @abstractmethod
    def update_user_configuration(
        self, username: str, req: UpdateUserConfigurationsRequestDto
    ):
        pass
