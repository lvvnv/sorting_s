# Упрощенный вариант (если не используется)
from django.http import HttpResponse

def classify_image(request):
    return HttpResponse("Classification will be here")

# import requests
# from django.shortcuts import render
# from .models import DetectionResult

# def detect_waste(request):
#     if request.method == 'POST':
#         image = request.FILES['image']
#         # Сохранение изображения (реализуйте согласно вашей структуре)
        
#         detector = Detector()
# detections = detector.detect(image.path)
        
#         for det in detections:
#             DetectionResult.objects.create(
#                 image=image_instance,
#                 x_min=det[0], y_min=det[1],
#                 x_max=det[2], y_max=det[3],
#                 confidence=det[4]
#             )

# # detection/views.py
# from django.http import HttpResponse

# def upload_image(request):
#     try:
#         return HttpResponse("Image upload form will be here")
#     except Exception as e:
#         error_message = f"Ошибка обработки изображения: {str(e)}",

# detection/views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from detection.detector import Detector
# from django.conf import settings
# import os
# import cv2
# import numpy as np
# from django.apps import apps
# import base64

# class DetectObjectsView(APIView):
#     """
#     API endpoint для детекции объектов на изображении
#     """
    
#     def post(self, request):
#         # Проверяем наличие изображения в запросе
#         if 'image' not in request.FILES:
#             return Response(
#                 {"error": "Изображение не предоставлено"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         try:
#             # Читаем изображение
#             image_file = request.FILES['image']
#             image_bytes = np.frombuffer(image_file.read(), np.uint8)
#             image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
            
#             if image is None:
#                 return Response(
#                     {"error": "Не удалось прочитать изображение"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
            
#             image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Конвертируем в RGB
            
#             # Инициализируем детектор
#             detector = Detector()
            
#             # Выполняем детекцию
#             detections = detector.predict(image)
            
#             # Если объекты не обнаружены
#             if not detections:
#                 return Response(
#                     {"error": "На изображении не обнаружено объектов"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
            
#             # Рисуем результаты на изображении
#             processed_image = detector.draw_detections(image.copy(), detections)
            
#             # Сохраняем обработанное изображение во временный файл
#             _, buffer = cv2.imencode('.jpg', cv2.cvtColor(processed_image, cv2.COLOR_RGB2BGR))
#             processed_image_base64 = base64.b64encode(buffer).decode('utf-8')
            
#             # Формируем данные для ответа
#             response_data = {
#                 "detections": [
#                     {
#                         "class": detection['class'],
#                         "confidence": detection['confidence'],
#                         "box": detection['box']
#                     }
#                     for detection in detections
#                 ],
#                 "processed_image_base64": f"data:image/jpeg;base64,{processed_image_base64}"
#             }
            
#             return Response(response_data, status=status.HTTP_200_OK)
            
#         except Exception as e:
#             import logging
#             logger = logging.getLogger(__name__)
#             logger.error(f"Ошибка при детекции объектов: {str(e)}")
            
#             return Response(
#                 {"error": "Ошибка при обнаружении объектов"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
