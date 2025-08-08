from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import os
import cv2
import numpy as np
from .models import UploadedImage
from django.db import transaction
from django.apps import apps
from .serializers import UploadedImageSerializer
from django.core.files.base import ContentFile
from io import BytesIO
import base64

class EnsembleAPIView(APIView):
    """
    API endpoint для обработки изображений: детекция и классификация
    """
    
    def post(self, request):
        # Проверяем наличие изображения в запросе
        if 'image' not in request.FILES:
            return Response(
                {"error": "Изображение не предоставлено"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Сохраняем загруженное изображение в транзакции
            with transaction.atomic():
                # Создаем экземпляр модели
                uploaded_image = UploadedImage(image=request.FILES['image'])
                uploaded_image.save()
            
            # Читаем изображение
            image_path = os.path.join(settings.MEDIA_ROOT, uploaded_image.image.name)
            image = cv2.imread(image_path)
            if image is None:
                return Response(
                    {"error": "Не удалось прочитать изображение"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Конвертируем в RGB
            
            # Инициализируем детектор
            detector = Detector()
            
            # Получаем классификатор из приложения classification
            classification_app = apps.get_app_config('classification')
            classifier = classification_app.classifier
            
            if not classifier.initialized:
                return Response(
                    {"error": "Модель классификации не загружена. Обратитесь к администратору."},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            
            # Выполняем детекцию
            detections = detector.predict(image)
            
            # Выполняем классификацию для каждого обнаруженного объекта
            for detection in detections:
                x1, y1, x2, y2 = detection['box']
                cropped_img = image[y1:y2, x1:x2]
                
                # Пропускаем слишком маленькие объекты
                if cropped_img.size == 0 or cropped_img.shape[0] < 10 or cropped_img.shape[1] < 10:
                    detection['classification_class'] = "too_small"
                    detection['classification_confidence'] = 0.0
                    continue
                
                # Классификация объекта
                class_name, confidence = classifier.predict(cropped_img)
                detection['classification_class'] = class_name
                detection['classification_confidence'] = confidence
            
            # Если объекты не обнаружены
            if not detections:
                return Response(
                    {"error": "На изображении не обнаружено объектов"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Рисуем результаты на изображении
            processed_image = detector.draw_detections(image.copy(), detections)
            
            # Сохраняем обработанное изображение
            processed_image_name = f"processed_{os.path.basename(uploaded_image.image.name)}"
            processed_image_path = os.path.join(settings.MEDIA_ROOT, 'debug', processed_image_name)
            
            # Создаем директорию, если она не существует
            os.makedirs(os.path.dirname(processed_image_path), exist_ok=True)
            
            cv2.imwrite(processed_image_path, cv2.cvtColor(processed_image, cv2.COLOR_RGB2BGR))
            
            # Обновляем запись в базе данных
            with transaction.atomic():
                uploaded_image.processed_image.name = os.path.join('debug', processed_image_name)
                uploaded_image.save()
            
            # Подготовка данных для ответа
            # Конвертируем изображения в base64 для включения в JSON (опционально)
            # Или возвращаем URL-ы для загрузки изображений отдельно
            response_data = {
                "original_image_url": request.build_absolute_uri(uploaded_image.image.url),
                "processed_image_url": request.build_absolute_uri(uploaded_image.processed_image.url),
                "detections": [
                    {
                        "detection_class": detection['class'],
                        "detection_confidence": detection['confidence'],
                        "classification_class": detection['classification_class'],
                        "classification_confidence": detection['classification_confidence'],
                        "box": detection['box']
                    }
                    for detection in detections
                ]
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Ошибка при обработке изображения: {str(e)}")
            
            return Response(
                {"error": f"Ошибка при обработке изображения: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        