import os
import numpy as np
import tensorflow as tf
from PIL import Image

CLASS_NAMES = ['Angry', 'Fear', 'Happy', 'Sad', 'Suprise']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ai_model",
    "emotion_model.keras"
)

# Global model variable
model = None


def load_model():
    global model

    if model is None:
        print("=" * 50)
        print("Loading Emotion Detection Model...")
        print("=" * 50)

        model = tf.keras.models.load_model(MODEL_PATH)

        print("Model Loaded Successfully!")
        print("=" * 50)

    return model


def preprocess_image(image):
    image = image.convert("RGB")
    image = image.resize((224, 224))
    image = np.array(image, dtype=np.float32)
    image = np.expand_dims(image, axis=0)
    return image


def predict_emotion(image):
    model = load_model()

    image = preprocess_image(image)

    predictions = model.predict(image, verbose=0)

    predicted_index = np.argmax(predictions[0])

    emotion = CLASS_NAMES[predicted_index]
    confidence = float(predictions[0][predicted_index] * 100)

    probabilities = {}

    for i, label in enumerate(CLASS_NAMES):
        probabilities[label] = round(float(predictions[0][i] * 100), 2)

    return emotion, confidence, probabilities
