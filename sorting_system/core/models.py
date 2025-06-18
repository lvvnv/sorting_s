from django.db import models
from django.conf import settings
import os

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    processed_image = models.ImageField(upload_to='debug/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return os.path.basename(self.image.name)