from abc import ABC, abstractmethod

from dtos.generate_audio_file_request_dto import GenerateAudioFileRequestDto
from dtos.generate_audio_file_response_dto import GenerateAudioFileResponseDto
from dtos.get_voices_response_dto import GetVoicesResponseDto


class IVoicesService(ABC):
    @abstractmethod
    def get_voices(self) -> GetVoicesResponseDto:
        pass

    @abstractmethod
    def generate_audio_file(
        self, req: GenerateAudioFileRequestDto
    ) -> GenerateAudioFileResponseDto:
        pass
