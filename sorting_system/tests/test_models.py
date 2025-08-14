# tests/test_models.py
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from core.models import UploadedImage
from classification.models import ClassificationResult
from detection.models import DetectionResult

@pytest.mark.django_db
class TestModels:
    """Test cases for models."""

    def test_uploaded_image_creation(self):
        """Test UploadedImage model creation."""
        # Create a simple image file
        image_content = b"fake image content"
        image_file = SimpleUploadedFile(
            "test_image.jpg",
            image_content,
            content_type="image/jpeg"
        )
        
        uploaded_image = UploadedImage.objects.create(
            image=image_file
        )
        
        assert uploaded_image.id is not None
        assert str(uploaded_image) == "test_image.jpg"
        assert "test_image.jpg" in uploaded_image.image.name

    def test_classification_result_creation(self):
        """Test ClassificationResult model creation."""
        # Create an uploaded image first
        image_content = b"fake image content"
        image_file = SimpleUploadedFile(
            "test_image.jpg",
            image_content,
            content_type="image/jpeg"
        )
        
        uploaded_image = UploadedImage.objects.create(
            image=image_file
        )
        
        # Create classification result
        classification_result = ClassificationResult.objects.create(
            image=uploaded_image,
            material="plastic",
            confidence=0.95
        )
        
        assert classification_result.id is not None
        assert classification_result.material == "plastic"
        assert classification_result.confidence == 0.95
        assert classification_result.image == uploaded_image

    def test_detection_result_creation(self):
        """Test DetectionResult model creation."""
        # Create an uploaded image first
        image_content = b"fake image content"
        image_file = SimpleUploadedFile(
            "test_image.jpg",
            image_content,
            content_type="image/jpeg"
        )
        
        uploaded_image = UploadedImage.objects.create(
            image=image_file
        )
        
        # Create detection result
        detection_result = DetectionResult.objects.create(
            image=uploaded_image,
            x_min=10,
            y_min=20,
            x_max=100,
            y_max=200,
            confidence=0.85
        )
        
        assert detection_result.id is not None
        assert detection_result.x_min == 10
        assert detection_result.y_min == 20
        assert detection_result.x_max == 100
        assert detection_result.y_max == 200
        assert detection_result.confidence == 0.85
        assert detection_result.image == uploaded_image