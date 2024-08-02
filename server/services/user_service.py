from flask_injector import inject


from utils.responses_helper import ok
from repositories.user_repository import UserRepository
from .interfaces.user_service import IUserService
from dtos.get_user_profile_dto import GetUserProfileResponseDto


class UserService(IUserService):
    @inject
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def get_profile(self, username: str) -> GetUserProfileResponseDto:
        user = self._user_repository.get_user_by_username(username)
        response = GetUserProfileResponseDto(
            name=user["name"],
            surname=user["surname"],
            phone_number=user["phone_number"],
            email=user["email"],
        ).model_dump()
        return ok(response)
