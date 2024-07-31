import os

from injector import Binder, singleton

from .interfaces.voices_service import IVoicesService
from .voices_service import VoicesService
from .interfaces.s3_service import IS3Service
from .s3_service import S3Service
from .interfaces.cognito_service import ICognitoService
from .cognito_service import CognitoService
from .interfaces.auth_service import IAuthService
from .auth_service import AuthService


def configure_di(binder: Binder) -> Binder:
    # Bind services from different modules
    binder.bind(
        IS3Service, to=S3Service(os.getenv("S3_BUCKET_NAME", "lipia")), scope=singleton
    )
    binder.bind(
        ICognitoService,
        to=CognitoService(
            os.getenv("AWS_COGNITO_USERS_POOL_ID"),
            os.getenv("AWS_COGNITO_USERS_CLIENT_ID"),
        ),
        scope=singleton,
    )
    binder.bind(
        IVoicesService,
        to=VoicesService,
        scope=singleton,
    )
    binder.bind(IAuthService, to=AuthService, scope=singleton)
