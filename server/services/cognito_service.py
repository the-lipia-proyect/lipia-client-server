import boto3
import hmac, hashlib, base64
import os
from typing import Dict, Any
from botocore.exceptions import ClientError

from .interfaces.cognito_service import ICognitoService

COGNITO_SECRET = os.getenv("AWS_COGNITO_SECRET")


class CognitoService(ICognitoService):
    def __init__(
        self,
        pool_id: str,
        client_id: str,
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    ):
        """
        Initialize the S3 client.

        Args:
            pool_id: (str): The AWS Cognito pool_id
            region_name (str, optional): The AWS region name (e.g., "us-east-1"). If not specified, it will use the default region from the environment.
        """
        self._cognito_client = boto3.client("cognito-idp", region_name=region_name)
        self._pool_id = pool_id
        self._client_id = client_id

    def authenticate_user(self, email: str, password: str):
        secret_hash = self.get_secret_hash(email)
        auth_params = {
            "USERNAME": email,
            "PASSWORD": password,
            "SECRET_HASH": secret_hash,
        }

        try:
            response = self._cognito_client.admin_initiate_auth(
                UserPoolId=self._pool_id,
                ClientId=self._client_id,
                AuthFlow="ADMIN_USER_PASSWORD_AUTH",
                AuthParameters=auth_params,
            )
            return response["AuthenticationResult"]
        except ClientError as error:
            if error.response["Error"]["Code"] == "NotAuthorizedException":
                raise ValueError("Invalid username or password")
            else:
                raise error

    def register_user(self, register_user_dto: Dict[str, Any]):
        attributes = [
            {"Name": "given_name", "Value": register_user_dto.get("name")},
            {"Name": "family_name", "Value": register_user_dto.get("surname")},
            {"Name": "email", "Value": register_user_dto.get("email")},
            {"Name": "phone_number", "Value": register_user_dto.get("phone_number")},
        ]
        secret_hash = self.get_secret_hash(register_user_dto["username"])
        try:
            signup_response = self._cognito_client.sign_up(
                ClientId=self._client_id,
                Username=register_user_dto["username"],
                Password=register_user_dto["password"],
                UserAttributes=attributes,
                SecretHash=secret_hash,
            )
            return signup_response["UserSub"]
        except ClientError as error:
            if error.response["Error"]["Code"] == "UsernameExistsException":
                raise ValueError("Email already exists")
            else:
                raise error

    def resend_confirmation_code(self, email: str):
        """Resends the confirmation code to the specified email address.

        Args:
            email (str): The email address of the user.

        Raises:
            ClientError: An error occurred while interacting with AWS Cognito.
        """
        secret_hash = self.get_secret_hash(email)
        try:
            self._cognito_client.resend_confirmation_code(
                ClientId=self._client_id, Username=email, SecretHash=secret_hash
            )
        except ClientError as error:
            raise error

    def verify_user(
        self,
        email: str,
        code: str,
    ):
        """Verifies the user's account using the provided confirmation code.

        Args:
            email (str): The email address of the user.
            code (str): The confirmation code sent to the user's email address.

        Raises:
            ClientError: An error occurred while interacting with AWS Cognito.
        """

        try:
            self._cognito_client.confirm_sign_up(
                ClientId=self._client_id,
                Username=email,
                ConfirmationCode=code,
                SecretHash=self.get_secret_hash(email),
            )
        except ClientError as error:
            print(f"Client Error: {error}")
            raise error

    def refresh_token(self, email: str, refresh_token: str):
        """Refreshes an existing user's access token using a refresh token.

        Args:
            refresh_token (str): The refresh token to use for refreshing the access token.
            client_id (str, optional): The client ID of your user pool. Defaults to the value set in the constructor.

        Raises:
            ClientError: An error occurred while interacting with AWS Cognito.

        Returns:
            dict: The response from the Cognito `initiate_auth` call, containing the refreshed access token information.
        """

        try:
            response = self._cognito_client.initiate_auth(
                ClientId=self._client_id,
                AuthFlow="REFRESH_TOKEN_AUTH",
                AuthParameters={
                    "REFRESH_TOKEN": refresh_token,
                    "SECRET_HASH": self.get_secret_hash(email),
                },
            )
            return response["AuthenticationResult"]
        except ClientError as error:
            raise error

    def forgot_password(self, email: str):
        """Sends a forgot password request to the specified email address.

        Args:
            email (str): The email address of the user.

        Raises:
            ClientError: An error occurred while interacting with AWS Cognito.
        """

        try:
            response = self._cognito_client.forgot_password(
                ClientId=self._client_id,
                Username=email,
                SecretHash=self.get_secret_hash(email),
            )
            return response
        except ClientError as error:
            raise error

    def confirm_forgot_password(self, email: str, password: str, code: str):
        """Confirms a forgotten password using the provided confirmation code and sets a new password.

        Args:
            email (str): The email address of the user.
            password (str): The new password to set for the user.
            code (str): The confirmation code sent to the user's email address.

        Raises:
            ClientError: An error occurred while interacting with AWS Cognito.
        """

        try:
            return self._cognito_client.confirm_forgot_password(
                ClientId=self._client_id,
                Username=email,
                Password=password,
                ConfirmationCode=code,
                SecretHash=self.get_secret_hash(email),
            )
        except ClientError as error:
            raise error

    def change_password(
        self, access_token: str, new_password: str, actual_password: str
    ) -> None:
        """Changes the password for a Cognito user asynchronously.

        Args:
            access_token (str): The user's access token.
            new_password (str): The new password for the user.
            actual_password (str): The user's current password.

        Raises:
            ClientError: If there are errors interacting with the Cognito service.
        """
        try:
            response = self._cognito_client.change_password(
                AccessToken=access_token,
                ProposedPassword=new_password,
                PreviousPassword=actual_password,
            )
            print("Password changed successfully!")
            return response

        except ClientError as error:
            print(f"Error changing password: {error}")
            raise error

    def logout(self, access_token: str):
        """Logs out the user by invalidating the access token.

        Args:
            access_token (str): The access token of the user.

        Raises:
            ClientError: If there are errors interacting with the Cognito service.
        """
        try:
            self._cognito_client.global_sign_out(AccessToken=access_token)
            print("User logged out successfully!")
        except ClientError as error:
            print(f"Error logging out: {error}")
            raise error

    def update_user(self, username: str, update_user_dto: Dict[str, Any]):
        """Updates user attributes in Cognito.

        Args:
            username (str): The username of the user.
            user_attributes (Dict[str, str]): A dictionary of user attributes to update.

        Raises:
            ClientError: If there are errors interacting with the Cognito service.
        """

        try:
            attributes = [
                {"Name": "given_name", "Value": update_user_dto.get("name")},
                {"Name": "family_name", "Value": update_user_dto.get("surname")},
            ]
            if update_user_dto.get("phone_number"):
                attributes.append(
                    {
                        "Name": "phone_number",
                        "Value": update_user_dto.get("phone_number"),
                    },
                )
            response = self._cognito_client.admin_update_user_attributes(
                UserPoolId=self._pool_id, Username=username, UserAttributes=attributes
            )
            return response
        except ClientError as error:
            print(f"Error updating user attributes: {error}")
            raise error

    def get_secret_hash(self, email: str):
        hashed_cognito_secret = bytes(COGNITO_SECRET, "utf-8")
        message = bytes(f"{email}{self._client_id}", "utf-8")
        return base64.b64encode(
            hmac.new(hashed_cognito_secret, message, digestmod=hashlib.sha256).digest()
        ).decode()
