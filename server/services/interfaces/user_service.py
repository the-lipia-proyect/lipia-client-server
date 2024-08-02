from abc import ABC, abstractmethod

from dtos.get_user_profile_dto import GetUserProfileResponseDto
from dtos.update_user_profile_request_dto import UpdateUserProfileRequestDto


class IUserService(ABC):
    @abstractmethod
    def get_profile(self, email: str) -> GetUserProfileResponseDto:
        pass

    @abstractmethod
    def update_profile(self, username: str, req: UpdateUserProfileRequestDto):
        pass
