from PIL import Image
import json
import base64
import cv2
import numpy as np
from io import BytesIO
from django.http import JsonResponse
from django.shortcuts import render
from .forms import ImageUploadForm
from .predictor import predict_emotion
from django.core.files.storage import FileSystemStorage
from .predictor import predict_emotion
from .face_detector import detect_face
from detector.face_landmarks import detect_landmarks
from detector.face_landmarks import detect_landmarks

def home(request):
    return render(request, "home.html")

def upload_image(request):
    

    emotion = None
    confidence = None
    probabilities = None
    image_url = None

    if request.method == "POST":

        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():

            # Get uploaded image
            uploaded_image = request.FILES["image"]

            # Save image to media/uploads
            fs = FileSystemStorage()

            filename = fs.save(f"uploads/{uploaded_image.name}", uploaded_image)

            image_url = fs.url(filename)

            # Open image for prediction
            image = Image.open(uploaded_image)

            # Predict emotion
            emotion, confidence, probabilities = predict_emotion(image)

    else:

        form = ImageUploadForm()

    context = {
        "form": form,
        "emotion": emotion,
        "confidence": confidence,
        "probabilities": probabilities,
        "image_url": image_url,
    }

    return render(
        request,
        "upload.html",
        context
    )

def webcam(request):
    return render(request, "webcam.html")

                base64.b64decode(image_data)
            )
        ).convert("RGB")

        # --------------------------------
        # 1. Face Detection
        # --------------------------------

def predict_live(request):

    if request.method == "POST":

        try:

            data = json.loads(request.body)

            image_data = data["image"]

            # Remove "data:image/jpeg;base64," part
            image_data = image_data.split(",")[1]

            # Decode image
            image = Image.open(
                BytesIO(
                    base64.b64decode(image_data)
                )
            ).convert("RGB")

            # --------------------------------
            # 1. FACE DETECTION
            # --------------------------------

            face, bbox = detect_face(image)

            # No face detected
            if face is None:

                return JsonResponse({
                    "face_detected": False,
                    "emotion": None,
                    "confidence": 0,
                    "probabilities": {},
                    "bbox": None,
                    "landmarks": []
                })

            # --------------------------------
            # 2. EMOTION PREDICTION
            # --------------------------------

            emotion, confidence, probabilities = predict_emotion(
                face
            )

            # --------------------------------
            # 3. RESPONSE
            # --------------------------------

            return JsonResponse({

                "face_detected": True,

                "emotion": emotion,

                "confidence": round(
                    confidence,
                    2
                ),

                "probabilities": probabilities,

                "bbox": bbox,

                # Landmarks temporarily disabled
                "landmarks": []

            })

        except Exception as e:

            print("LIVE PREDICTION ERROR:", str(e))

            return JsonResponse({

                "error": str(e),

                "face_detected": False,

                "emotion": None,

                "confidence": 0,

                "probabilities": {},

                "bbox": None,

                "landmarks": []

            }, status=500)

    return JsonResponse({
        "error": "Invalid Request"
    }, status=400)
