# detection/urls.py
from django.urls import path
from . import views

app_name = 'detection'

urlpatterns = [
    path('upload/', views.upload_image, name='upload'),
]