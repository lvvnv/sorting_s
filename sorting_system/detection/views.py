import requests
from django.shortcuts import render
from .models import DetectionResult

def detect_waste(request):
    if request.method == 'POST':
        image = request.FILES['image']
        # Сохранение изображения (реализуйте согласно вашей структуре)
        
        detector = MarbageDetector()
        detections = detector.detect(image.path)
        
        for det in detections:
            DetectionResult.objects.create(
                image=image_instance,
                x_min=det[0], y_min=det[1],
                x_max=det[2], y_max=det[3],
                confidence=det[4]
            )

# detection/views.py
from django.http import HttpResponse

def upload_image(request):
    try:
        return HttpResponse("Image upload form will be here")
    except Exception as e:
        error_message = f"Ошибка обработки изображения: {str(e)}"