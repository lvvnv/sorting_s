from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ClassificationSerializer

class ClassifyAPIView(APIView):
    def post(self, request):
        # Здесь вызов модели или внешнего API
        data = {
            "class_name": "пластик",
            "confidence": 0.92
        }
        serializer = ClassificationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)