# sorting_system/core/urls.py
from django.urls import path
from .views import ensemble_view

urlpatterns = [
    path('', ensemble_view, name='ensemble'),
]