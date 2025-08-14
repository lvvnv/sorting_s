# tests/test_api_views.py
import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch, MagicMock
import json

@pytest.mark.django_db
class TestAPIViews:
    """Test cases for API views."""

    def test_classify_api_view_get(self, api_client):
        """Test that GET request to classify endpoint returns 405."""
        url = reverse('api:classify')
        response = api_client.get(url)
        assert response.status_code == 405  # Method not allowed

    def test_detect_api_view_get(self, api_client):
        """Test that GET request to detect endpoint returns 405."""
        url = reverse('api:detect')
        response = api_client.get(url)
        assert response.status_code == 405  # Method not allowed

    @patch('api.views.apps.get_app_config')
    def test_classify_api_view_post_no_image(self, mock_get_app_config, api_client):
        """Test that POST request without image returns 400."""
        # Mock the classifier app config
        mock_app_config = MagicMock()
        mock_app_config.classifier.initialized = True
        mock_get_app_config.return_value = mock_app_config
        
        url = reverse('api:classify')
        response = api_client.post(url, {})
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data

    @patch('api.views.apps.get_app_config')
    def test_detect_api_view_post_no_image(self, mock_get_app_config, api_client):
        """Test that POST request without image returns 400."""
        # Mock the detection app config
        mock_app_config = MagicMock()
        mock_get_app_config.return_value = mock_app_config
        
        url = reverse('api:detect')
        response = api_client.post(url, {})
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data

    def test_classify_api_view_delete_requires_image_id(self, api_client):
        """Test that DELETE request without image_id returns 404."""
        url = reverse('api:delete_classification', kwargs={'image_id': 99999})
        response = api_client.delete(url)
        # Should return 404 for non-existent image
        assert response.status_code == 404

    def test_detect_api_view_delete_requires_image_id(self, api_client):
        """Test that DELETE request without image_id returns 404."""
        url = reverse('api:delete_detection', kwargs={'image_id': 99999})
        response = api_client.delete(url)
        # Should return 404 for non-existent image
        assert response.status_code == 404