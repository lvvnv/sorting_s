from django.urls import path
from .views import EnsembleAPIView

urlpatterns = [
    path('api/ensemble/', EnsembleAPIView.as_view(), name='ensemble'),
]