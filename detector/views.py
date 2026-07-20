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

def predict_live(request):

    if request.method == "POST":

        data = json.loads(request.body)

        image_data = data["image"]

        # Remove the Base64 header
        image_data = image_data.split(",")[1]

        image = Image.open(
            BytesIO(base64.b64decode(image_data))
        )

        emotion, confidence, probabilities = predict_emotion(image)

        return JsonResponse({
            "emotion": emotion,
            "confidence": round(confidence, 2),
            "probabilities": probabilities
        })

    return JsonResponse({"error": "Invalid Request"})