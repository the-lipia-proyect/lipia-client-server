from flask_injector import inject

from utils.responses_helper import ok
from .interfaces.available_models_service import IAvailableModelsService
from dtos.get_available_models_response_dto import GetAvailableModelsResponseDto
from utils.modelutils import VALID_MODELS


class AvailableModelsService(IAvailableModelsService):
    @inject
    def __init__(self):
        pass

    def get_available_models(self) -> GetAvailableModelsResponseDto:
        response = GetAvailableModelsResponseDto(models=VALID_MODELS)
        return ok(response)
