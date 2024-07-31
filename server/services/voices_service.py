import os
import http
from io import BytesIO
import uuid

from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from flask_injector import inject

from dtos.generate_audio_file_request_dto import GenerateAudioFileRequestDto
from dtos.generate_audio_file_response_dto import GenerateAudioFileResponseDto
from dtos.get_voices_response_dto import GetVoicesResponseDto, VoiceDto
from dtos.generate_audio_file_request_dto import GenerateAudioFileRequestDto
from dtos.generate_audio_file_response_dto import GenerateAudioFileResponseDto
from utils.api_caller import api_caller
from utils.responses_helper import ok
from .interfaces.voices_service import IVoicesService
from .interfaces.s3_service import IS3Service

ELEVEN_LABS_URL = os.getenv("ELEVEN_LABS_API_URL")
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
eleven_labs_client = ElevenLabs(
    api_key=ELEVEN_LABS_API_KEY,
)
# ENGLISH VERSION
# MODEL_ID = "eleven_turbo_v2"
MODEL_ID = "eleven_multilingual_v2"
AUDIO_FILES_PATH = "prediction_audios"


class VoicesService(IVoicesService):
    @inject
    def __init__(self, s3_service: IS3Service) -> None:
        self._s3_service = s3_service

    def get_voices(self) -> GetVoicesResponseDto:
        headers = {
            "Accept": "application/json",
            "xi-api-key": os.getenv("ELEVEN_LABS_API_KEY"),
            "Content-Type": "application/json",
        }

        response = api_caller(
            method=http.HTTPMethod.GET,
            url=f"{ELEVEN_LABS_URL}/voices",
            headers=headers,
        )

        voices_response = GetVoicesResponseDto(
            voices=[
                VoiceDto(voice_id=item["voice_id"], name=item["name"])
                for item in response["voices"]
            ]
        ).model_dump()

        return ok(voices_response)

    def generate_audio_file(self, req: GenerateAudioFileRequestDto):
        text_to_speech_response = eleven_labs_client.text_to_speech.convert(
            voice_id=req.voice_id,
            optimize_streaming_latency="3",
            output_format="mp3_22050_32",
            text=req.text,
            model_id=MODEL_ID,  # use the turbo model for low latency, for other languages use the `eleven_multilingual_v2`
            voice_settings=VoiceSettings(
                stability=req.voice_settings.stability,
                similarity_boost=req.voice_settings.similarity_boost,
                style=req.voice_settings.style,
                use_speaker_boost=True,
            ),
        )
        audio_stream = BytesIO()
        for chunk in text_to_speech_response:
            if chunk:
                audio_stream.write(chunk)

        audio_stream.seek(0)

        s3_file_name = f"{uuid.uuid4()}.mp3"
        file_full_path = f"{AUDIO_FILES_PATH}/{s3_file_name}"
        self._s3_service.upload_file(file_full_path, audio_stream)
        presigned_url = self._s3_service.generate_presigned_url(
            "get_object",
            file_full_path,
        )
        response = GenerateAudioFileResponseDto(file_url=presigned_url).model_dump()
        return ok(response)
