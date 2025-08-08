from django.urls import path
from .views import ClassifyAPIView

urlpatterns = [
    path('classify/', ClassifyAPIView.as_view(), name='classify'),
]