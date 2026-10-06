import os
import mediapipe as mp


# Project root
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# Face Landmarker model
MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "face_landmarker.task"
)


# MediaPipe classes
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode


# Landmarker configuration
options = FaceLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),
    running_mode=RunningMode.IMAGE,
    num_faces=1
)


# Create landmarker
landmarker = FaceLandmarker.create_from_options(
    options
)


def detect_landmarks(mp_image):

    result = landmarker.detect(mp_image)

    if not result.face_landmarks:
        return None

    return result.face_landmarks[0]