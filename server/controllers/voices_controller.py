import http
import os
import uuid
from io import BytesIO

from flask import Blueprint, request
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from flask_cognito import cognito_auth_required

from utils.api_caller import api_caller
from utils.s3_connector import S3Utils
from utils.responses_helper import ok, bad_request, internal_server_error


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

    voices = {
        "voices": [
            {"voice_id": item["voice_id"], "name": item["name"]}
            for item in response["voices"]
        ]
    }

    return ok(voices)


@bp.route("/text-to-speech", methods=[http.HTTPMethod.POST])
@cognito_auth_required
def generate_audio_file():
    body = request.get_json()
    text = body.get("text")
    voice_id = body.get("voice_id")
    if not text:
        return bad_request({"message": "Invalid body: missing 'text' key"})
    if not voice_id:
        return bad_request({"message": "Invalid body: missing 'voice_id' key"})
    try:
        text_to_speech_response = eleven_labs_client.text_to_speech.convert(
            voice_id=voice_id,
            optimize_streaming_latency="3",
            output_format="mp3_22050_32",
            text=text,
            model_id=MODEL_ID,  # use the turbo model for low latency, for other languages use the `eleven_multilingual_v2`
            voice_settings=VoiceSettings(
                stability=0.5,
                similarity_boost=0.95,
                style=0.0,
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
        response = {"file_url": presigned_url}
        return ok(response)
    except Exception as e:
        return internal_server_error({"message": e.__str__()})
