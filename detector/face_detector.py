import os
import numpy as np
from PIL import Image

import mediapipe as mp


# --------------------------------------------------
# MODEL PATH
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "blaze_face_short_range.tflite"
)


# --------------------------------------------------
# CREATE FACE DETECTOR
# --------------------------------------------------

BaseOptions = mp.tasks.BaseOptions
FaceDetector = mp.tasks.vision.FaceDetector
FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
RunningMode = mp.tasks.vision.RunningMode


options = FaceDetectorOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),
    running_mode=RunningMode.IMAGE,
    min_detection_confidence=0.5
)

detector = FaceDetector.create_from_options(options)


# --------------------------------------------------
# DETECT FACE
# --------------------------------------------------

def detect_face(image):

    """
    Detect the first face in a PIL image.

    Returns:
        face_image
        bbox
    """

    # Convert to RGB
    image = image.convert("RGB")

    # Convert PIL → NumPy
    image_np = np.array(image)

    # Convert NumPy → MediaPipe Image
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=image_np
    )

    # Detect faces
    result = detector.detect(mp_image)

    # No face
    if not result.detections:
        return None, None

    # First face
    detection = result.detections[0]

    bounding_box = detection.bounding_box

    x = bounding_box.origin_x
    y = bounding_box.origin_y

    width = bounding_box.width
    height = bounding_box.height

    # Image dimensions
    image_height, image_width, _ = image_np.shape

    # Padding
    padding = 20

    x1 = max(0, x - padding)
    y1 = max(0, y - padding)

    x2 = min(
        image_width,
        x + width + padding
    )

    y2 = min(
        image_height,
        y + height + padding
    )

    # Crop face
    face = image_np[
        y1:y2,
        x1:x2
    ]

    if face.size == 0:
        return None, None

    # Convert back to PIL
    face_image = Image.fromarray(face)

    bbox = {
        "x": x1,
        "y": y1,
        "width": x2 - x1,
        "height": y2 - y1
    }

    return face_image, bbox