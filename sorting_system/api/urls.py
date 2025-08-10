from django.urls import path, include
from .views import ClassifyAPIView, DetectObjectsView

urlpatterns = [
    path('classify/', ClassifyAPIView.as_view(), name='classify'),
    path('detect/', DetectObjectsView.as_view(), name='detect'),
]