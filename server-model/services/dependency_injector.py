from injector import Binder, singleton

from .interfaces.predictions_service import IPredictionsService
from .interfaces.available_models_service import IAvailableModelsService
from .predictions_service import PredictionsService
from .available_models_service import AvailableModelsService


def configure_di(binder: Binder) -> Binder:
    binder.bind(IPredictionsService, to=PredictionsService, scope=singleton)
    binder.bind(IAvailableModelsService, to=AvailableModelsService, scope=singleton)
