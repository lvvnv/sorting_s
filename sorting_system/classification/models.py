from django.db import models
from detection.models import DetectionResult

class ClassificationResult(models.Model):
    detection = models.OneToOneField(DetectionResult, on_delete=models.CASCADE)
    material = models.CharField(max_length=50)  # e.g., plastic, glass
    confidence = models.FloatField()
    classified_at = models.DateTimeField(auto_now_add=True)