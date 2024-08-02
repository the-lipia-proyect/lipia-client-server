from abc import ABC, abstractmethod

from dtos.login_request_dto import LoginRequestDto
from dtos.login_response_dto import LoginResponseDto
from dtos.sign_up_request_dto import SignUpRequestDto
from dtos.sign_up_response_dto import SignUpResponseDto
from dtos.verification_code_resend_request_dto import VerificationCodeResendRequestDto
from dtos.email_verification_request_dto import EmailVerificationRequestDto
from dtos.refresh_token_dto import RefreshTokenRequestDto
from dtos.refresh_token_response_dto import RefreshTokenResponseDto
from dtos.forgot_password_request_dto import ForgotPasswordRequestDto
from dtos.forgot_password_confirmation_request_dto import (
    ForgotPasswordConfirmationRequestDto,
)
from dtos.change_password_request_dto import ChangePasswordRequestDto


class IAuthService(ABC):
    @abstractmethod
    def login(self, req: LoginRequestDto) -> LoginResponseDto:
        pass

    @abstractmethod
    def sign_up(self, req: SignUpRequestDto) -> SignUpResponseDto:
        pass

    @abstractmethod
    def resend_email_confirmation_code(self, req: VerificationCodeResendRequestDto):
        pass

    @abstractmethod
    def verify_email(self, req: EmailVerificationRequestDto):
        pass

    @abstractmethod
    def refresh_token(
        self, username: str, req: RefreshTokenRequestDto
    ) -> RefreshTokenResponseDto:
        pass

    @abstractmethod
    def forgot_password(self, req: ForgotPasswordRequestDto):
        pass

    @abstractmethod
    def forgot_password_confirmation(self, req: ForgotPasswordConfirmationRequestDto):
        pass

    @abstractmethod
    def change_password(self, access_token: str, req: ChangePasswordRequestDto):
        pass

    @abstractmethod
    def logout(self, access_token: str):
        pass
