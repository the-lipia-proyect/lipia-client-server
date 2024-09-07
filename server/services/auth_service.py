from flask_injector import inject

from utils.responses_helper import ok
from dtos.login_request_dto import LoginRequestDto
from dtos.login_response_dto import LoginResponseDto, LoginAuthResponseDto
from dtos.sign_up_request_dto import SignUpRequestDto
from dtos.sign_up_response_dto import SignUpResponseDto
from dtos.verification_code_resend_request_dto import VerificationCodeResendRequestDto
from dtos.email_verification_request_dto import EmailVerificationRequestDto
from dtos.refresh_token_dto import RefreshTokenRequestDto
from dtos.refresh_token_response_dto import (
    RefreshTokenResponseDto,
    RefreshTokenAuthResponseDto,
)
from dtos.forgot_password_request_dto import ForgotPasswordRequestDto
from dtos.forgot_password_confirmation_request_dto import (
    ForgotPasswordConfirmationRequestDto,
)
from dtos.change_password_request_dto import ChangePasswordRequestDto
from .interfaces.cognito_service import ICognitoService
from .interfaces.auth_service import IAuthService
from repositories.user_repository import UserRepository


class AuthService(IAuthService):
    @inject
    def __init__(
        self, cognito_service: ICognitoService, user_repository: UserRepository
    ):
        self._cognito_service = cognito_service
        self._user_repository = user_repository

    def login(self, req: LoginRequestDto) -> LoginResponseDto:
        authenticate_user_response = self._cognito_service.authenticate_user(
            req.username, req.password
        )
        response = LoginResponseDto(
            auth=LoginAuthResponseDto(
                access_token=authenticate_user_response.get("AccessToken"),
                expiration_date=authenticate_user_response.get("ExpiresIn"),
                id_token=authenticate_user_response.get("IdToken"),
                refresh_token=authenticate_user_response.get("RefreshToken"),
                token_type=authenticate_user_response.get("TokenType"),
            )
        )
        return ok(response)

    def sign_up(self, req: SignUpRequestDto) -> SignUpResponseDto:
        register_user_dto = {
            "name": req.name,
            "surname": req.surname,
            "email": req.email,
            "phone_number": req.phone_number,
            "username": req.username,
            "password": req.password,
        }
        cognito_user_id = self._cognito_service.register_user(register_user_dto)
        db_user_id = self._user_repository.insert(cognito_user_id, req)
        return ok(SignUpResponseDto(id=db_user_id))

    def resend_email_confirmation_code(self, req: VerificationCodeResendRequestDto):
        self._cognito_service.resend_confirmation_code(req.email)
        return ok({})

    def verify_email(self, req: EmailVerificationRequestDto):
        self._cognito_service.verify_user(req.email, req.code)
        return ok({})

    def refresh_token(
        self, username: str, req: RefreshTokenRequestDto
    ) -> RefreshTokenResponseDto:
        refresh_token_response = self._cognito_service.refresh_token(
            username, req.refresh_token
        )
        response = RefreshTokenResponseDto(
            auth=RefreshTokenAuthResponseDto(
                access_token=refresh_token_response.get("AccessToken"),
                expiration_date=refresh_token_response.get("ExpiresIn"),
                id_token=refresh_token_response.get("IdToken"),
                token_type=refresh_token_response.get("TokenType"),
            )
        )
        return ok(response)

    def forgot_password(self, req: ForgotPasswordRequestDto):
        self._cognito_service.forgot_password(req.username)
        return ok({})

    def forgot_password_confirmation(self, req: ForgotPasswordConfirmationRequestDto):
        self._cognito_service.confirm_forgot_password(
            req.username, req.password, req.code
        )
        return ok({})

    def change_password(self, access_token: str, req: ChangePasswordRequestDto):
        # TODO: Add auth token as the first parameter
        self._cognito_service.change_password(
            access_token,
            req.new_password,
            req.actual_password,
        )
        return ok({})

    def logout(self, access_token: str):
        self._cognito_service.logout(access_token)
        return ok({})
