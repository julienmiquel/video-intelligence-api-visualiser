import time
import os

from google.cloud import videointelligence
 
video_client = videointelligence.VideoIntelligenceServiceClient()
 
OUTPUT_BUCKET  = os.environ.get("OUTPUT_BUCKET")

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
 
speech_config = videointelligence.SpeechTranscriptionConfig(
    language_code="en-US",
    enable_automatic_punctuation=True,
)
 
person_config = videointelligence.PersonDetectionConfig(
    include_bounding_boxes=True,
    include_attributes=False,
    include_pose_landmarks=True,
)
 
face_config = videointelligence.FaceDetectionConfig(
    include_bounding_boxes=True,
    include_attributes=True,
)
 
video_context = videointelligence.VideoContext(
    speech_transcription_config=speech_config,
    person_detection_config=person_config,
    face_detection_config=face_config,
)
 
 
def analyze_video(event, context):
    print(event)
 
    input_uri = "gs://" + event["bucket"] + "/" + event["name"]
    file_stem = event["name"].split(".")[0]
    output_uri = f"{OUTPUT_BUCKET}/{file_stem} - {time.time()}.json"
    
    print(f"input_uri = {input_uri} - output_uri = {output_uri} file_stem = {file_stem}")
    language_code="en-US"
    #if the input_uri contain "en-US" set the language_code variable to "en-US"
    if "en-US" in input_uri:
        language_code="en-US"
        
    if "fr-FR" in input_uri:        
        language_code="fr-FR"
        
    if "es-ES" in input_uri:        
        language_code="es-ES"   
        
    if "de-DE" in input_uri:        
        language_code="de-DE"

    if "it-IT" in input_uri:        
        language_code="it-IT"

    if "pt-PT" in input_uri:        
        language_code="pt-PT"

    if "pt-BR" in input_uri:        
        language_code="pt-BR"

    if "zh-CN" in input_uri:        
        language_code="zh-CN"

    if "ja-JP" in input_uri:        
        language_code="ja-JP"

    if "ko-KR" in input_uri:        
        language_code="ko-KR"

    if "ar-XA" in input_uri:        
        language_code="ar-XA"

    if "ru-RU" in input_uri:        
        language_code="ru-RU"

    if "hi-IN" in input_uri:        
        language_code="hi-IN"
        
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