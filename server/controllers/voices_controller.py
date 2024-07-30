import http
import os
import uuid
from io import BytesIO

from flask import Blueprint, request
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from flask_cognito import cognito_auth_required
from pydantic import ValidationError

from utils.api_caller import api_caller
from utils.s3_connector import S3Utils
from utils.responses_helper import ok, bad_request, internal_server_error
from dtos.get_voices_response_dto import GetVoicesResponseDto, VoiceDto
from dtos.generate_audio_file_request_dto import GenerateAudioFileRequestDto
from dtos.generate_audio_file_response_dto import GenerateAudioFileResponseDto


bp = Blueprint("voices", __name__, url_prefix="/voices")

ELEVEN_LABS_URL = os.getenv("ELEVEN_LABS_API_URL")
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
eleven_labs_client = ElevenLabs(
    api_key=ELEVEN_LABS_API_KEY,
)
# ENGLISH VERSION
# MODEL_ID = "eleven_turbo_v2"
MODEL_ID = "eleven_multilingual_v2"
AUDIO_FILES_PATH = "prediction_audios"
s3_client = S3Utils(os.getenv("S3_BUCKET_NAME", "lipia"))


@bp.route(None, methods=[http.HTTPMethod.GET])
@cognito_auth_required
def get_voices():
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


@bp.route("/text-to-speech", methods=[http.HTTPMethod.POST])
@cognito_auth_required
def generate_audio_file():
    try:
        req = GenerateAudioFileRequestDto(**request.get_json())
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
        s3_client.upload_file(file_full_path, audio_stream)
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            file_full_path,
        )
        response = GenerateAudioFileResponseDto(file_url=presigned_url).model_dump()
        return ok(response)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})
