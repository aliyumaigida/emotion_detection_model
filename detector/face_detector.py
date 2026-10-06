import cv2
import numpy as np
from PIL import Image


# --------------------------------------------------
# OPENCV FACE DETECTOR
# --------------------------------------------------

FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def detect_face(image):
    """
    Detect the first face in a PIL image.

    Returns:
        face_image: cropped PIL image
        bbox: dictionary containing face coordinates
    """

    # Make sure image is RGB
    image = image.convert("RGB")

    # Convert PIL image to NumPy
    image_np = np.array(image)

    # Convert RGB → grayscale
    gray = cv2.cvtColor(
        image_np,
        cv2.COLOR_RGB2GRAY
    )

    # Detect faces
    faces = FACE_CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50)
    )

    # No face found
    if len(faces) == 0:
        return None, None

    # Use the first detected face
    x, y, width, height = faces[0]

    # Padding around face
    padding = 20

    x1 = max(0, x - padding)
    y1 = max(0, y - padding)

    x2 = min(
        image_np.shape[1],
        x + width + padding
    )

    y2 = min(
        image_np.shape[0],
        y + height + padding
    )

    # Crop face
    face = image_np[
        y1:y2,
        x1:x2
    ]

    # Make sure crop is valid
    if face.size == 0:
        return None, None

    # Convert NumPy → PIL
    face_image = Image.fromarray(face)

    # Bounding box
    bbox = {
        "x": int(x1),
        "y": int(y1),
        "width": int(x2 - x1),
        "height": int(y2 - y1)
    }

    return face_image, bbox
