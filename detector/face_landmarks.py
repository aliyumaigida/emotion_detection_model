import os
import mediapipe as mp


# --------------------------------------------------
# PROJECT ROOT
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# --------------------------------------------------
# FACE LANDMARKER MODEL
# --------------------------------------------------

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "face_landmarker.task"
)


# --------------------------------------------------
# MEDIAPIPE CONFIGURATION
# --------------------------------------------------

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode


# --------------------------------------------------
# LANDMARKER
# --------------------------------------------------

landmarker = None


def get_landmarker():
    """
    Create the MediaPipe Face Landmarker only
    when it is actually needed.
    """

    global landmarker

    if landmarker is None:

        options = FaceLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path=MODEL_PATH
            ),
            running_mode=RunningMode.IMAGE,
            num_faces=1
        )

        landmarker = FaceLandmarker.create_from_options(
            options
        )

    return landmarker


# --------------------------------------------------
# DETECT LANDMARKS
# --------------------------------------------------

def detect_landmarks(mp_image):

    # Get the landmarker
    face_landmarker = get_landmarker()

    # Detect landmarks
    result = face_landmarker.detect(mp_image)

    # No face landmarks found
    if not result.face_landmarks:
        return None

    # Return landmarks for the first face
    return result.face_landmarks[0]
