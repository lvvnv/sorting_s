# tests/test_urls.py
import pytest
from django.urls import reverse, resolve
from api.views import ClassifyAPIView, DetectObjectsView

class TestURLs:
    """Test cases for URL routing."""

    def test_classify_url_resolves(self):
        """Test that classify URL resolves to ClassifyAPIView."""
        url = reverse('api:classify')
        resolver = resolve(url)
        assert resolver.func.view_class == ClassifyAPIView

    def test_detect_url_resolves(self):
        """Test that detect URL resolves to DetectObjectsView."""
        url = reverse('api:detect')
        resolver = resolve(url)
        assert resolver.func.view_class == DetectObjectsView

    def test_delete_classification_url_resolves(self):
        """Test that delete classification URL resolves correctly."""
        url = reverse('api:delete_classification', kwargs={'image_id': 1})
        resolver = resolve(url)
        assert resolver.func.view_class == ClassifyAPIView
        assert resolver.kwargs['image_id'] == '1'

    def test_delete_detection_url_resolves(self):
        """Test that delete detection URL resolves correctly."""
        url = reverse('api:delete_detection', kwargs={'image_id': 1})
        resolver = resolve(url)
        assert resolver.func.view_class == DetectObjectsView
        assert resolver.kwargs['image_id'] == '1'