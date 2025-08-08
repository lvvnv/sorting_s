from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ClassificationSerializer
from django.apps import apps
import cv2
import numpy as np

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
            # data = {
            #     "class_name": "пластик",
            #     "confidence": 0.92
            # }
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
            print(data)
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
        