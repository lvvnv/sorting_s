from django.db import models
from core.models import UploadedImage

class ClassificationResult(models.Model):
    image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE)
    material = models.CharField(max_length=50)  # e.g., plastic, glass
    confidence = models.FloatField()
    classified_at = models.DateTimeField(auto_now_add=True)
    is_wrong = models.BooleanField(default=False)  # New field to mark misclassifications