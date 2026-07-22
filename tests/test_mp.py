import cv2
import pytest
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

@pytest.mark.skip(reason="Needs local image and dependencies")
def test_mp():
    frame = cv2.imread(".venv/lib/python3.14/site-packages/ultralytics/assets/zidane.jpg")
    if frame is None:
        return
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    print("Testing IMAGE mode")
    base_options = python.BaseOptions(model_asset_path='models/face_landmarker.task')
    options = vision.FaceLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.IMAGE,
        num_faces=1
    )
    landmarker = vision.FaceLandmarker.create_from_options(options)
    processed = landmarker.detect(mp_image)
    print("IMAGE mode faces:", len(processed.face_landmarks) if processed.face_landmarks else 0)

    print("Testing VIDEO mode")
    options_vid = vision.FaceLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_faces=1
    )
    landmarker_vid = vision.FaceLandmarker.create_from_options(options_vid)
    processed_vid = landmarker_vid.detect_for_video(mp_image, 1000)
    print("VIDEO mode faces:", len(processed_vid.face_landmarks) if processed_vid.face_landmarks else 0)
