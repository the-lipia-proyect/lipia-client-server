from io import BytesIO
import uuid
import time
from urllib.parse import urlparse

from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from flask_injector import inject

from dtos.generate_audio_file_request_dto import GenerateAudioFileRequestDto
from dtos.generate_audio_file_response_dto import GenerateAudioFileResponseDto
from dtos.get_voices_response_dto import GetVoicesResponseDto, VoiceDto
from dtos.generate_audio_file_request_dto import GenerateAudioFileRequestDto
from dtos.generate_audio_file_response_dto import GenerateAudioFileResponseDto
from dtos.generate_voice_request_dto import GenerateVoiceRequestDto
from dtos.generate_voice_response_dto import GenerateVoiceResponseDto
from utils.responses_helper import ok, not_found
from .interfaces.voices_service import IVoicesService
from .interfaces.s3_service import IS3Service
from utils.api_caller import api_caller
from repositories.user_voices_repository import UserVoiceRepository

# ENGLISH VERSION
# MODEL_ID = "eleven_turbo_v2"
MODEL_ID = "eleven_multilingual_v2"
AUDIO_FILES_PATH = "prediction_audios"
CLONED_VOICES_AUDIOS_PATH = "cloned_voices_audios"


class VoicesService(IVoicesService):
    @inject
    def __init__(
        self,
        s3_service: IS3Service,
        eleven_labs_service: ElevenLabs,
        user_voices_repository: UserVoiceRepository,
    ) -> None:
        self._s3_service = s3_service
        self._eleven_labs_service = eleven_labs_service
        self._user_voices_repository = user_voices_repository

    def get_voices(self, user_id: str) -> GetVoicesResponseDto:
        response = self._eleven_labs_service.voices.get_all()
        user_voices = self._user_voices_repository.get_by_user_id(user_id)
        user_voice_ids = {voice.get("_id") for voice in user_voices}
        eleven_labs_voices = response.voices
        # This array contains eleven labs premade or professional predefined voices
        premade_or_professional_voices = [
            voice
            for voice in eleven_labs_voices
            if voice.category in ["premade", "professional"]
        ]
        # This array contains voices generated with out user
        cloned_voices = [
            voice for voice in eleven_labs_voices if voice.category == "cloned"
        ]
        user_cloned_voices = [
            voice for voice in cloned_voices if voice.voice_id in user_voice_ids
        ]
        user_visible_voices = premade_or_professional_voices + user_cloned_voices
        voices_response = GetVoicesResponseDto(
            voices=[
                VoiceDto(voice_id=item.voice_id, name=item.name)
                for item in user_visible_voices
            ]
        )

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

        response = GenerateAudioFileResponseDto(file_url=file_url)
        return ok(response)

    def create_voice(self, user_id: str, req: GenerateVoiceRequestDto):
        final_files = []

        for audio_url in req.audios:
            parsed_url = urlparse(audio_url)
            source_key = parsed_url.path.lstrip("/")

            destination_key = f"{CLONED_VOICES_AUDIOS_PATH}/{source_key.split('/')[-1]}"

            self._s3_service.move_file(source_key, destination_key)

            final_url = f"https://{self._s3_service.bucket_name}.s3.amazonaws.com/{destination_key}"

            response = api_caller("GET", headers={}, url=final_url)

            file_content = BytesIO(response.content)
            final_files.append(file_content)
        add_voice_response = self._eleven_labs_service.voices.add(
            name=req.name, files=final_files
        )

        self._user_voices_repository.insert(user_id, add_voice_response.voice_id)

        response = GenerateVoiceResponseDto(id=add_voice_response.voice_id)
        return ok(response)

    def delete_voice(self, user_id: str, id: str):
        existing_user_voice = (
            self._user_voices_repository.get_user_voice_by_user_id_and_id(user_id, id)
        )

        if not existing_user_voice:
            return not_found({"message": "The voice does not exist"})
        delete_voice_response = self._eleven_labs_service.voices.delete(voice_id=id)
        self._user_voices_repository.delete(id)
        return ok({})
