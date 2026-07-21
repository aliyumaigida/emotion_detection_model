# 🎭 Real-Time Human Emotion Detection System

> A production-ready deep learning application that detects human facial emotions from uploaded images using **TensorFlow**, **MobileNetV2**, **Django REST Framework**, and **Render**.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?logo=tensorflow)
![Django](https://img.shields.io/badge/Django-Framework-green?logo=django)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap)
![Render](https://img.shields.io/badge/Deployment-Render-success)

---

# Live Demo

**Try the application here:**

https://emotion-detection-model-sdn1.onrender.com

The application allows users to:

- Upload a facial image
- Predict one of five human emotions
- View confidence scores
- View probability distribution for each emotion
- Display an emoji corresponding to the detected emotion

---

# Project Overview

This project demonstrates the complete machine learning lifecycle, from data collection and preprocessing to model deployment in a production-ready web application.

The objective is to automatically recognize human facial emotions from images using Transfer Learning with MobileNetV2 and deploy the trained model as a Django web application.

Recognized emotions include:

- 😀 Happy
- 😢 Sad
- 😠 Angry
- 😨 Fear
- 😲 Surprise

Unlike many academic projects that stop after model training, this project covers the entire AI workflow, including cloud deployment.

---

# 🎯 Objectives

- Build a facial emotion recognition model using Deep Learning.
- Apply Transfer Learning to improve model performance.
- Evaluate model performance using multiple metrics.
- Deploy the trained model as a web application.
- Allow users to upload images and receive predictions in real time.

---

# Dataset

The dataset was obtained from Kaggle and consists of **59,099 facial images** across five emotion categories.

## Dataset Distribution

| Emotion | Images |
|----------|-------:|
| Happy | 18,439 |
| Sad | 12,553 |
| Angry | 10,148 |
| Fear | 9,732 |
| Surprise | 8,227 |

**Total Images:** **59,099**

---

# Data Exploration

Before training, the dataset was inspected to:

- Verify image quality
- Check class distribution
- Detect class imbalance
- Visualize sample images from each emotion

This analysis helped determine whether additional techniques such as class weighting and data augmentation were necessary.

---

# Data Preprocessing

The following preprocessing steps were applied:

- Image resizing to **224 × 224**
- RGB conversion
- MobileNetV2 preprocessing
- Train / Validation / Test split

To improve generalization, data augmentation was applied:

- Random Horizontal Flip
- Random Rotation
- Random Zoom
- Random Contrast
- Random Translation

---

# Model Development

Instead of building a CNN from scratch, this project uses **Transfer Learning**.

## Backbone Network

**MobileNetV2 (ImageNet Pretrained)**

Architecture:

Input Image (224×224×3)
        │
        ▼
Data Augmentation
        │
        ▼
MobileNetV2
        │
        ▼
GlobalAveragePooling2D
        │
        ▼
Dropout
        │
        ▼
Dense Layer (Softmax)
        │
        ▼
Emotion Prediction


Transfer Learning significantly reduced training time while improving performance.


# Model Training

Training was performed using:

- Google Colab GPU
- TensorFlow
- Keras
- Jupyter Notebook

Training techniques included:

- EarlyStopping
- ModelCheckpoint
- ReduceLROnPlateau
- Class Weights

These techniques helped reduce overfitting and improve convergence.



# Model Evaluation

The model was evaluated using:

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

### Performance Summary

| Metric | Score |
|---------|-------|
| Accuracy | ~60% |
| Precision | ~59% |
| Recall | ~59% |
| F1-Score | ~59% |

Although the overall accuracy is moderate, the confusion matrix showed strong performance for Happy and Surprise while Fear remained the most challenging class.

# Confusion Matrix Analysis

The confusion matrix revealed several important observations:

- Happy achieved the highest recognition accuracy.
- Surprise was recognized reliably.
- Fear was frequently confused with Sad.
- Angry was occasionally confused with Sad.

These misclassifications are expected because several human emotions share similar facial expressions.

Rather than relying solely on overall accuracy, the model was also evaluated using Precision, Recall, and F1-Score to obtain a more comprehensive understanding of its performance.

---

# ⚠ Challenges Encountered

## 1. Dataset Imbalance

Although the dataset contained over 59,000 images, it was not perfectly balanced.

Happy contained over **18,000 images**, while Surprise contained approximately **8,200 images**.

This imbalance caused the model to learn Happy more effectively than the smaller classes.

To reduce this problem, the following techniques were used:

- Class Weights
- Data Augmentation
- Transfer Learning
- Multiple Evaluation Metrics

---

## 2. Emotion Similarity

Some facial expressions naturally resemble one another.

Examples include:

- Fear ↔ Sad
- Angry ↔ Sad
- Fear ↔ Angry

These similarities resulted in unavoidable classification errors despite fine-tuning.

---

## 3. Model Comparison

Different transfer learning models were explored.

Models investigated included and later remove the EfficientNetB0:

- MobileNetV2
- EfficientNetB0

Although EfficientNetB0 was tested, MobileNetV2 achieved better overall performance on this dataset while providing faster inference and a smaller model size.

Therefore, MobileNetV2 was selected for deployment.

---

## 4. Deployment Challenges

Deploying a TensorFlow model in production introduced several practical challenges.

Examples included:

- Managing TensorFlow dependencies
- Loading large model files
- Configuring Django static files
- Production deployment on Render

Successfully resolving these issues provided valuable hands-on experience with machine learning deployment.

---

# Model Export

After training, the best-performing model was exported as:

```
emotion_mobilenetv2.keras
```

This model is loaded directly by the Django application during prediction.

---

# Django Web Application

The trained model was integrated into a Django application.

Current features include:

- Image Upload
- Emotion Prediction
- Confidence Score
- Emotion Probability Distribution
- Dynamic Emoji Display
- Responsive Bootstrap Interface

---

# Deployment

The complete application was successfully deployed on **Render**.

Deployment stack:

- Django
- Gunicorn
- WhiteNoise
- TensorFlow
- Render

The deployed application performs inference on uploaded images in real time.


# Technologies Used

## Machine Learning

- Python
- TensorFlow
- Keras
- MobileNetV2
- NumPy
- Pillow
- Scikit-learn

## Backend

- Django
- Django REST Framework

## Frontend

- HTML
- CSS
- Bootstrap
- JavaScript

## Deployment

- Render
- Gunicorn
- WhiteNoise

## Development Environment

- Google Colab
- Jupyter Notebook
- Visual Studio Code
- Git
- GitHub

---

# Repository Structure

emotion-detection-system/

│
├── ai_model/
│   └── emotion_model.keras
│
├── detector/
│
├── notebooks/
│   └── Emotion_Detection_Training.ipynb
│
├── screenshots/
│   ├── home.png
│   ├── upload.png
│   ├── prediction.png
│   ├── confusion_matrix.png
│   ├── training_accuracy.png
│   └── training_loss.png
│
├── static/
├── media/
├── requirements.txt
├── LICENSE
├── README.md
└── manage.py

# Screenshots

The repository contains screenshots of:

- Home Page
- Upload Interface
- Prediction Result
- Emotion Probability Distribution
- Confusion Matrix
- Training Accuracy Curve
- Training Loss Curve

---

# Training Notebook

The complete model development process is documented inside the `notebooks` folder.

The notebook includes:

- Data Loading
- Data Exploration
- Preprocessing
- Data Augmentation
- Transfer Learning
- Fine-Tuning
- Model Evaluation
- Confusion Matrix
- Model Export

---

# Future Improvements

Planned enhancements include:

- Real-time webcam emotion detection
- Face detection before emotion recognition
- Video emotion recognition
- Emotion history logging
- Docker containerization
- TensorFlow Lite deployment
- CI/CD pipeline
- Improved dataset balancing

---

# Lessons Learned

This project strengthened my practical understanding of:

- Deep Learning
- Transfer Learning
- Computer Vision
- Dataset Preparation
- Hyperparameter Tuning
- Model Evaluation
- Confusion Matrix Analysis
- Django Development
- Machine Learning Deployment
- Cloud Deployment

It also reinforced the importance of dataset quality, class balance, and proper evaluation when building production-ready AI systems.


# About Me

I am passionate about Artificial Intelligence, Machine Learning, Computer Vision, and Backend Development.

I enjoy building end-to-end AI applications that move beyond experimentation into production deployment.

My goal is to continue developing practical AI solutions that solve real-world problems while continuously expanding my skills in Data science, Machine Learning and Machine Learning Operations.


# ⭐ Support

If you found this project useful or interesting, please consider giving it a ⭐ on GitHub.

Feedback, suggestions, and contributions are always welcome.
