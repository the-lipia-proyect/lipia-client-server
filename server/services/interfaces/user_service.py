from abc import ABC, abstractmethod

from dtos.get_user_profile_dto import GetUserProfileResponseDto


class IUserService(ABC):
    @abstractmethod
    def get_profile(self, email: str) -> GetUserProfileResponseDto:
        pass
