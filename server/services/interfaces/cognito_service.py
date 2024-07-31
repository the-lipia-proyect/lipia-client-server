from abc import ABC, abstractmethod
from typing import Dict, Any


class ICognitoService(ABC):
    @abstractmethod
    def authenticate_user(self, email: str, password: str):
        pass

    @abstractmethod
    def register_user(self, register_user_dto: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def resend_confirmation_code(self, email: str):
        pass

    @abstractmethod
    def verify_user(
        self,
        email: str,
        code: str,
    ):
        pass

    @abstractmethod
    def refresh_token(self, email: str, refresh_token: str):
        pass

    @abstractmethod
    def forgot_password(self, email: str):
        pass

    @abstractmethod
    def confirm_forgot_password(self, email: str, password: str, code: str):
        pass

    @abstractmethod
    def change_password(
        self, access_token: str, new_password: str, actual_password: str
    ) -> None:
        pass
