import cv2
import base64
import logging
from django.shortcuts import render
from .forms import ImageUploadForm
from .models import UploadedImage
from detection.detector import detect_waste

logger = logging.getLogger(__name__)

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Сохраняем загруженное изображение
                uploaded_image = form.save()
                
                # Реальная детекция и классификация
                detections = detect_waste(uploaded_image.image.path)
                
                # Генерируем base64 для ROI
                for det in detections:
                    _, buffer = cv2.imencode('.jpg', det['roi'])
                    det['roi_base64'] = base64.b64encode(buffer).decode('utf-8')
                
                return render(request, 'core/results.html', {
                    'original_image': uploaded_image,
                    'detections': detections
                })
            
            except Exception as e:
                logger.error(f"Ошибка обработки изображения: {str(e)}")
                return render(request, 'core/error.html', {
                    'error': f"Ошибка обработки изображения: {str(e)}"
                })
    else:
        form = ImageUploadForm()
    return render(request, 'core/upload.html', {'form': form})