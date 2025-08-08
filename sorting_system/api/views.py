from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ClassificationSerializer
from django.apps import apps

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
            data = {
                "class_name": "пластик",
                "confidence": 0.92
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
        