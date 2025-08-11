from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ClassificationSerializer, DetectionResponseSerializer
from django.apps import apps
import cv2
import numpy as np
import base64

class ClassifyAPIView(APIView):
    def post(self, request):
        # Проверяем наличие изображения в запросе
        if 'image' not in request.FILES:
            return Response(
                {"error": "Изображение не предоставлено"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Получаем загруженное изображение
        image = request.FILES['image']
        
        try:
            classification_app = apps.get_app_config('classification')
            classifier = classification_app.classifier
            
            # Проверяем, инициализирован ли классификатор
            if not classifier.initialized:
                return Response(
                    {"error": "Модель классификации не загружена. Обратитесь к администратору."},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            
            # Читаем изображение
            image_file = request.FILES['image']
            
            # Конвертируем файл в numpy array для классификатора
            image_bytes = np.frombuffer(image_file.read(), np.uint8)
            image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
            
            if image is None:
                return Response(
                    {"error": "Не удалось прочитать изображение"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Выполняем классификацию
            class_name, confidence = classifier.predict(image)

            data = {
                "class_name": class_name,
                "confidence": confidence
            }
            # Валидируем данные через сериализатор
            serializer = ClassificationSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            
            return Response(serializer.data)
            
        except Exception as e:
            # Логируем ошибку для отладки
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Ошибка при классификации изображения: {str(e)}")
            
            return Response(
                {"error": "Ошибка при обработке изображения (exception)"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        


class DetectObjectsView(APIView):    
    def post(self, request):
        # Проверяем наличие изображения в запросе
        if 'image' not in request.FILES:
            return Response(
                {"error": "Изображение не предоставлено"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Читаем изображение
            image_file = request.FILES['image']
            image_bytes = np.frombuffer(image_file.read(), np.uint8)
            image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
            
            if image is None:
                return Response(
                    {"error": "Не удалось прочитать изображение"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Конвертируем в RGB
            
            # Получаем детектор из конфигурации приложения
            detection_app = apps.get_app_config('detection')
            detector = detection_app.detector
            
            # Проверяем, инициализирован ли детектор
            # Note: The Detector class doesn't have an 'initialized' attribute like the Classifier.
            # We'll assume it's always initialized if we can get it from the app config.
            
            # Выполняем детекцию
            detections = detector.predict(image)
            
            # Если объекты не обнаружены
            if not detections:
                response_data = {
                    "detections": [
                        {
                            "class_name": "Нет",
                            "confidence": "0",
                            "box": [0, 0, 0, 0]
                        }
                    ],
                    "processed_image_base64": "0"
                }
                serializer = DetectionResponseSerializer(data=response_data)
                serializer.is_valid(raise_exception=True)
                
                return Response(serializer.data, status=status.HTTP_200_OK)
                # return Response(
                #     {"error": "На изображении не обнаружено объектов"},
                #     status=status.HTTP_400_BAD_REQUEST
                # )
            
            # Рисуем результаты на изображении
            processed_image = detector.draw_detections(image.copy(), detections)
            
            # Сохраняем обработанное изображение во временный файл
            _, buffer = cv2.imencode('.jpg', cv2.cvtColor(processed_image, cv2.COLOR_RGB2BGR))
            processed_image_base64 = base64.b64encode(buffer).decode('utf-8')
            
            # Формируем данные для ответа
            response_data = {
                "detections": [
                    {
                        "class_name": detection['class_name'],
                        "confidence": detection['confidence'],
                        "box": detection['box']
                    }
                    for detection in detections
                ],
                "processed_image_base64": f"data:image/jpeg;base64,{processed_image_base64}"
            }
            
            # Валидируем данные через сериализатор
            serializer = DetectionResponseSerializer(data=response_data)
            serializer.is_valid(raise_exception=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Ошибка при детекции объектов: {str(e)}")
            
            return Response(
                {"error": "Ошибка при обнаружении объектов"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
