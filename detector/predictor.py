import os
import numpy as np
import tensorflow as tf
from PIL import Image

# Emotion labels
CLASS_NAMES = ['Angry', 'Fear', 'Happy', 'Sad', 'Suprise']

# Project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Model path
MODEL_PATH = os.path.join(
    BASE_DIR,
    "ai_model",
    "emotion_model.keras"
)

print("=" * 50)
print("Loading Emotion Detection Model...")
print("=" * 50)

model = tf.keras.models.load_model(MODEL_PATH)
model.summary()

print("Model Loaded Successfully!")
print("=" * 50)


def preprocess_image(image):
    """
    Prepare image for prediction.
    IMPORTANT:
    The trained model already contains the MobileNetV2
    preprocessing layer, so DO NOT call
    tf.keras.applications.mobilenet_v2.preprocess_input()
    again.
    """

    # Convert to RGB
    image = image.convert("RGB")

    # Resize
    image = image.resize((224, 224))

    # Convert to NumPy
    image = np.array(image, dtype=np.float32)

    # Add batch dimension
    image = np.expand_dims(image, axis=0)

    return image


def predict_emotion(image):
    """
    Predict emotion from a PIL image.
    """

    image = preprocess_image(image)

    predictions = model.predict(image, verbose=0)

    predicted_index = np.argmax(predictions[0])

    emotion = CLASS_NAMES[predicted_index]

    confidence = float(predictions[0][predicted_index] * 100)

    probabilities = {}

    for i, label in enumerate(CLASS_NAMES):
        probabilities[label] = round(
            float(predictions[0][i] * 100), 2
        )

    return emotion, confidence, probabilities
