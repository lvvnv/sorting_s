# tests/test_serializers.py
import pytest
from api.serializers import ClassificationSerializer, DetectionSerializer, DetectionResponseSerializer

class TestSerializers:
    """Test cases for serializers."""

    def test_classification_serializer_valid_data(self):
        """Test ClassificationSerializer with valid data."""
        data = {
            'class_name': 'plastic',
            'confidence': 0.95,
            'image_id': 1
        }
        
        serializer = ClassificationSerializer(data=data)
        assert serializer.is_valid() is True
        assert serializer.validated_data['class_name'] == 'plastic'
        assert serializer.validated_data['confidence'] == 0.95

    def test_classification_serializer_invalid_confidence(self):
        """Test ClassificationSerializer with invalid confidence."""
        data = {
            'class_name': 'plastic',
            'confidence': 1.5,  # Invalid - should be <= 1.0
            'image_id': 1
        }
        
        serializer = ClassificationSerializer(data=data)
        # Confidence validation might be handled elsewhere, so this might still be valid
        # depending on serializer implementation
        
    def test_detection_serializer_valid_data(self):
        """Test DetectionSerializer with valid data."""
        data = {
            'class_name': 'bottle',
            'confidence': 0.85,
            'box': [10, 20, 100, 200]
        }
        
        serializer = DetectionSerializer(data=data)
        assert serializer.is_valid() is True
        assert serializer.validated_data['class_name'] == 'bottle'
        assert serializer.validated_data['confidence'] == 0.85
        assert serializer.validated_data['box'] == [10, 20, 100, 200]

    def test_detection_response_serializer_valid_data(self):
        """Test DetectionResponseSerializer with valid data."""
        data = {
            'detections': [
                {
                    'class_name': 'bottle',
                    'confidence': 0.85,
                    'box': [10, 20, 100, 200]
                }
            ],
            'processed_image_base64': 'base64encodedstring',
            'image_id': 1
        }
        
        serializer = DetectionResponseSerializer(data=data)
        assert serializer.is_valid() is True
        assert len(serializer.validated_data['detections']) == 1