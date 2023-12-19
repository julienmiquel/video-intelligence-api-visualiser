import time
 
from google.cloud import videointelligence
 
video_client = videointelligence.VideoIntelligenceServiceClient()
 
OUTPUT_BUCKET = "gs://YOUR OUTPUT BUCKET NAME"
 
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
 
    video_client.annotate_video(
        request={
            "features": features,
            "input_uri": input_uri,
            "output_uri": output_uri,
            "video_context": video_context,
        }
    )
 
    print("Processing video ", input_uri)