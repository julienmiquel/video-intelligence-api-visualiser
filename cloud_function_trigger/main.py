import time
import os

from google.cloud import videointelligence

video_client = videointelligence.VideoIntelligenceServiceClient()

OUTPUT_BUCKET = os.environ.get("OUTPUT_BUCKET")

PROJECT_ID = "ml-demo-384110"
REGION = "us-central1"


def write_to_bucket(bucket_name, file_name, input):
    """Writes the input to a file in the specified bucket.

    Args:
    bucket_name: The name of the bucket to write to.
    file_name: The name of the file to write to.
    input: The input to write to the file.

    Returns:
    The name of the file that was written to.
    """
    from google.cloud import storage

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    blob.upload_from_string(input)

    return blob.name


#############################
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from google.api_core.client_options import ClientOptions
from google.cloud import speech_v2

client = SpeechClient(    client_options=ClientOptions(api_endpoint=f"{REGION}-speech.googleapis.com"))

def get_recognizer(recognizer_id: str, language_code : str):

    try:
        # Initialize request argument(s)
        request = speech_v2.GetRecognizerRequest(        name=recognizer_id,        )
        recognizer = client.get_recognizer(request)
        # Handle the response
        print(recognizer)
        return recognizer
    except Exception as e:
        print(e)
        print("Error getting recognizer. Create new one.")

    recognizer_request = cloud_speech.CreateRecognizerRequest(
        parent=f"projects/{PROJECT_ID}/locations/{REGION}",
        recognizer_id=recognizer_id,
        recognizer=cloud_speech.Recognizer(
            language_codes=[language_code],
            model="chirp",
        ),
    )
    client.get_recognizer(recognizer_id)
    create_operation = client.create_recognizer(request=recognizer_request)
    recognizer = create_operation.result()

    return recognizer





def transcribe_gcs(gcs_uri_input: str, gcs_uri_output: str, language_code) -> str:
    """Asynchronously transcribes the audio file specified by the gcs_uri.

    Args:
        gcs_uri: The Google Cloud Storage path to an audio file.

    Returns:
        The generated transcript from the audio file provided.
    """
    from google.cloud.speech_v2 import SpeechClient
    from google.cloud.speech_v2.types import cloud_speech
    from google.api_core.client_options import ClientOptions

    client = SpeechClient(    client_options=ClientOptions(api_endpoint=f"{REGION}-speech.googleapis.com"))

    recognizer_id = f"chirp-{language_code.lower()}-test"
    recognizer = get_recognizer(recognizer_id, language_code    )

    print(f"Created recognizer: {recognizer.name}")

    long_audio_config = cloud_speech.RecognitionConfig(
        features=cloud_speech.RecognitionFeatures(
            enable_automatic_punctuation=True, enable_word_time_offsets=True
        ),
        auto_decoding_config={},
    )

    long_audio_request = cloud_speech.BatchRecognizeRequest(
        recognizer=recognizer.name,
        recognition_output_config={
            "gcs_output_config": {"uri": f"{gcs_uri_output}/transcriptions"}
        },
        files=[{"config": long_audio_config, "uri": gcs_uri_input}],
    )

    long_audio_operation = client.batch_recognize(request=long_audio_request)
    return 


def process_video(input_uri, output_uri, language_code):

    features = [
        videointelligence.Feature.OBJECT_TRACKING,
        videointelligence.Feature.LABEL_DETECTION,
        videointelligence.Feature.SHOT_CHANGE_DETECTION,
        videointelligence.Feature.SPEECH_TRANSCRIPTION,
        videointelligence.Feature.LOGO_RECOGNITION,
        videointelligence.Feature.EXPLICIT_CONTENT_DETECTION,
        videointelligence.Feature.TEXT_DETECTION,
        videointelligence.Feature.FACE_DETECTION,
        videointelligence.Feature.PERSON_DETECTION,
    ]

    person_config = videointelligence.PersonDetectionConfig(
        include_bounding_boxes=True,
        include_attributes=False,
        include_pose_landmarks=True,
    )
    face_config = videointelligence.FaceDetectionConfig(
        include_bounding_boxes=True,
        include_attributes=True,
    )
    speech_config = videointelligence.SpeechTranscriptionConfig(
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    video_context = videointelligence.VideoContext(
        speech_transcription_config=speech_config,
        person_detection_config=person_config,
        face_detection_config=face_config,
    )
    video_client.annotate_video(
        request={
            "features": features,
            "input_uri": input_uri,
            "output_uri": output_uri,
            "video_context": video_context,
        }
    )

    print("Processing video ", input_uri)


def process_stt(input_uri, output_uri, language_code):
    from pathlib import Path as p
    import librosa
    from IPython.display import Audio as play
    import pandas as pd
    from google.cloud.speech_v2 import SpeechClient
    from google.cloud.speech_v2.types import cloud_speech
    from google.api_core.client_options import ClientOptions
    import time
    import json
    import jiwer

    long_audio_uri = input_uri

    # long_audio_duration = librosa.get_duration(path=long_audio_path)
    # if long_audio_duration < 60:
    #     raise Exception(
    #         f"The audio is less than 1 min. Actual length: {long_audio_duration}"
    #     )


def analyze_video(event, context):
    print(event)

    input_uri = "gs://" + event["bucket"] + "/" + event["name"]
    file_stem = event["name"].split(".")[0]
    output_uri = f"{OUTPUT_BUCKET}/{file_stem} - {time.time()}.json"

    print(
        f"input_uri = {input_uri} - output_uri = {output_uri} file_stem = {file_stem}")
    language_code = "en-US"
    # if the input_uri contain "en-US" set the language_code variable to "en-US"
    if "en-US" in input_uri:
        language_code = "en-US"

    if "fr-FR" in input_uri:
        language_code = "fr-FR"

    if "es-ES" in input_uri:
        language_code = "es-ES"

    if "de-DE" in input_uri:
        language_code = "de-DE"

    if "it-IT" in input_uri:
        language_code = "it-IT"

    if "pt-PT" in input_uri:
        language_code = "pt-PT"

    if "pt-BR" in input_uri:
        language_code = "pt-BR"

    if "zh-CN" in input_uri:
        language_code = "zh-CN"

    if "ja-JP" in input_uri:
        language_code = "ja-JP"

    if "ko-KR" in input_uri:
        language_code = "ko-KR"

    if "ar-XA" in input_uri:
        language_code = "ar-XA"

    if "ru-RU" in input_uri:
        language_code = "ru-RU"

    if "hi-IN" in input_uri:
        language_code = "hi-IN"

    transcribe_gcs(input_uri, output_uri, language_code)
    #print("processing desactivated")
#    return
    # process_video(input_uri, output_uri, language_code)
    # process_stt()
