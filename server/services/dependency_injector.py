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
from .mongodb_service import MongoDBClient
from repositories.user_repository import UserRepository
from .interfaces.user_service import IUserService
from .user_service import UserService
from .interfaces.user_configurations_service import IUserConfigurationService
from .user_configurations_service import UserConfigurationService
from repositories.user_configurations_repository import UserConfigurationRepository
from .interfaces.shortcuts_service import IShortcutsService
from .shortcuts_service import ShortcutsService
from repositories.shortcuts_repository import ShortcutRepository


def configure_di(binder: Binder) -> Binder:
    # Bind services from different modules
    binder.bind(
        MongoDBClient,
        to=MongoDBClient(
            "lipia_database",
            os.getenv("MONGODB_USERNAME"),
            os.getenv("MONGODB_PASSWORD"),
            os.getenv("MONGODB_CLUSTER"),
        ),
        scope=singleton,
    )
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
    binder.bind(UserRepository, to=UserRepository, scope=singleton)
    binder.bind(IUserService, to=UserService, scope=singleton)
    binder.bind(IUserConfigurationService, to=UserConfigurationService, scope=singleton)
    binder.bind(
        UserConfigurationRepository, to=UserConfigurationRepository, scope=singleton
    )
    binder.bind(IShortcutsService, to=ShortcutsService, scope=singleton)
    binder.bind(ShortcutRepository, to=ShortcutRepository, scope=singleton)
