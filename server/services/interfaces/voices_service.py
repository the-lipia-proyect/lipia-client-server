from abc import ABC, abstractmethod

from dtos.generate_audio_file_request_dto import GenerateAudioFileRequestDto
from dtos.generate_audio_file_response_dto import GenerateAudioFileResponseDto
from dtos.get_voices_response_dto import GetVoicesResponseDto
from dtos.generate_voice_request_dto import GenerateVoiceRequestDto


class IVoicesService(ABC):
    @abstractmethod
    def get_voices(self, user_id: str) -> GetVoicesResponseDto:
        pass

    @abstractmethod
    def generate_audio_file(
        self, user_id: str, req: GenerateAudioFileRequestDto
    ) -> GenerateAudioFileResponseDto:
        pass

    @abstractmethod
    def create_voice(self, user_id: str, req: GenerateVoiceRequestDto):
        pass

    @abstractmethod
    def delete_voice(self, user_id: str, id: str):
        pass
