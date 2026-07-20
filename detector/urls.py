from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),

    path("upload/",views.upload_image,name="upload"),
    path("webcam/", views.webcam, name="webcam"),
    path("predict-live/", views.predict_live, name="predict_live"),

]