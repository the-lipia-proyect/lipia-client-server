from injector import Binder, singleton

from .interfaces.predictions_service import IPredictionsService
from .predictions_service import PredictionsService


def configure_di(binder: Binder) -> Binder:
    binder.bind(IPredictionsService, to=PredictionsService, scope=singleton)
