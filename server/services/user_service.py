from flask_injector import inject


from utils.responses_helper import ok, not_found
from repositories.user_repository import UserRepository
from .interfaces.cognito_service import ICognitoService
from .interfaces.user_service import IUserService
from dtos.get_user_profile_dto import GetUserProfileResponseDto
from dtos.update_user_profile_request_dto import UpdateUserProfileRequestDto


class UserService(IUserService):
    @inject
    def __init__(
        self, cognito_service: ICognitoService, user_repository: UserRepository
    ):
        self._cognito_service = cognito_service
        self._user_repository = user_repository

    def get_profile(self, username: str) -> GetUserProfileResponseDto:
        user = self._user_repository.get_user_by_username(username)
        if not user:
            return not_found({"message": "incorrect username"})
        response = GetUserProfileResponseDto(
            name=user["name"],
            surname=user["surname"],
            phone_number=user["phone_number"],
            email=user["email"],
        ).model_dump()
        return ok(response)

    def update_profile(self, username: str, req: UpdateUserProfileRequestDto):
        user = self._user_repository.get_user_by_username(username)
        if not user:
            return not_found({"message": "incorrect username"})
        update_user_dto = {"name": req.name, "surname": req.surname}
        if req.phone_number:
            update_user_dto.update({"phone_number": req.phone_number})
        cognito_update_user_response = self._cognito_service.update_user(
            username, update_user_dto
        )
        self._user_repository.update(user["_id"], req)
        return ok({})
