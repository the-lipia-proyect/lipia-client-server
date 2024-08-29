from io import BytesIO
import uuid
import time

from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from flask_injector import inject

from dtos.generate_audio_file_request_dto import GenerateAudioFileRequestDto
from dtos.generate_audio_file_response_dto import GenerateAudioFileResponseDto
from dtos.get_voices_response_dto import GetVoicesResponseDto, VoiceDto
from dtos.generate_audio_file_request_dto import GenerateAudioFileRequestDto
from dtos.generate_audio_file_response_dto import GenerateAudioFileResponseDto
from utils.responses_helper import ok
from .interfaces.voices_service import IVoicesService
from .interfaces.s3_service import IS3Service

# ENGLISH VERSION
# MODEL_ID = "eleven_turbo_v2"
MODEL_ID = "eleven_multilingual_v2"
AUDIO_FILES_PATH = "prediction_audios"


class VoicesService(IVoicesService):
    @inject
    def __init__(self, s3_service: IS3Service, eleven_labs_service: ElevenLabs) -> None:
        self._s3_service = s3_service
        self._eleven_labs_service = eleven_labs_service

    def get_voices(self) -> GetVoicesResponseDto:
        response = self._eleven_labs_service.voices.get_all()

        voices_response = GetVoicesResponseDto(
            voices=[
                VoiceDto(voice_id=item.voice_id, name=item.name)
                for item in response.voices
            ]
        ).model_dump()

        return ok(voices_response)

    def generate_audio_file(self, user_id: str, req: GenerateAudioFileRequestDto):
        current_time = time.gmtime()
        year = current_time.tm_year
        month = f"{current_time.tm_mon:02d}"
        day = f"{current_time.tm_mday:02d}"
        text_to_speech_response = self._eleven_labs_service.text_to_speech.convert(
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
        file_full_path = f"{AUDIO_FILES_PATH}/USER_ID={user_id}/YEAR={year}/MONTH={month}/DAY={day}/{s3_file_name}"
        self._s3_service.upload_file(file_full_path, audio_stream)
        file_url = (
            f"https://{self._s3_service.bucket_name}.s3.amazonaws.com/{file_full_path}"
        )

        response = GenerateAudioFileResponseDto(file_url=file_url).model_dump()
        return ok(response)
