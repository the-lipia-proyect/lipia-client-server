from abc import ABC, abstractmethod

from dtos.get_prediction_response_dto import GetPredictionResponseDto
from dtos.get_prediction_request_dto import GetPredictionRequestDto
from dtos.get_prediction_compressed_request_dto import GetPredictionCompressedRequestDto


class IPredictionsService(ABC):
    @abstractmethod
    def predict(self, req: GetPredictionRequestDto) -> GetPredictionResponseDto:
        pass

    @abstractmethod
    def predict_opencv(self, req: GetPredictionRequestDto) -> GetPredictionResponseDto:
        pass

    @abstractmethod
    def predict_compressed(
        self, req: GetPredictionCompressedRequestDto
    ) -> GetPredictionResponseDto:
        pass

    @abstractmethod
    def predict_compressed_opencv(
        self, req: GetPredictionCompressedRequestDto
    ) -> GetPredictionResponseDto:
        pass
