from abc import ABC, abstractmethod

from dtos.get_available_models_response_dto import GetAvailableModelsResponseDto


class IAvailableModelsService(ABC):
    @abstractmethod
    def get_available_models(self) -> GetAvailableModelsResponseDto:
        pass
