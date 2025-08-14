# from django.shortcuts import render
# from .forms import ImageUploadForm
# from detection.detector import Detector
# from django.conf import settings
# import os
# import cv2
# import numpy as np
# from .models import UploadedImage
# from django.db import transaction
# from django.apps import apps  # Импортируем apps для доступа к классификатору

# def ensemble_view(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             try:
#                 # Сохраняем загруженное изображение в транзакции
#                 with transaction.atomic():
#                     uploaded_image = form.save()
                
#                 # Читаем изображение
#                 image_path = os.path.join(settings.MEDIA_ROOT, uploaded_image.image.name)
#                 image = cv2.imread(image_path)
#                 image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Конвертируем в RGB
                
#                 if image is None:
#                     return render(request, 'core/error.html', {
#                         'message': 'Не удалось прочитать изображение'
#                     })
                
#                 # Инициализируем детектор
#                 detector = Detector()
                
#                 # Получаем классификатор из приложения classification
#                 classification_app = apps.get_app_config('classification')
#                 classifier = classification_app.classifier
                
#                 if not classifier.initialized:
#                     error_message = "Модель классификации не загружена. Обратитесь к администратору."
#                     return render(request, 'core/error.html', {'message': error_message})
                
#                 # Выполняем детекцию
#                 detections = detector.predict(image)
                
#                 # Выполняем классификацию
#                 classification_results = []

#                 # Для каждого обнаруженного объекта выполняем классификацию
#                 for detection in detections:
#                     x1, y1, x2, y2 = detection['box']
#                     cropped_img = image[y1:y2, x1:x2]
                    
#                     # Пропускаем слишком маленькие объекты
#                     if cropped_img.size == 0 or cropped_img.shape[0] < 10 or cropped_img.shape[1] < 10:
#                         detection['class'] = "too_small"
#                         detection['confidence'] = 0.0
#                         continue
                    
#                     # Классификация объекта
#                     class_name, confidence = classifier.predict(cropped_img)
#                     classification_results.append({
#                         'class': class_name,
#                         'confidence': confidence
#                     })
#                     # detection['class'] = class_name
#                     # detection['confidence'] = confidence
#                     # Добавляем результаты классификации в объект детекции
#                     detection['classification_class'] = class_name
#                     detection['classification_confidence'] = confidence
                
#                 if not detections:
#                     return render(request, 'core/no_detections.html')
                
#                 # Рисуем результаты на изображении
#                 processed_image = detector.draw_detections(image.copy(), detections)
                
#                 # Сохраняем обработанное изображение
#                 processed_image_name = f"processed_{os.path.basename(uploaded_image.image.name)}"
#                 processed_image_path = os.path.join(settings.MEDIA_ROOT, 'debug', processed_image_name)
#                 cv2.imwrite(processed_image_path, cv2.cvtColor(processed_image, cv2.COLOR_RGB2BGR))
                
#                 # Обновляем запись в базе данных
#                 with transaction.atomic():
#                     # Сохраняем только имя файла, а не объект ImageFieldFile
#                     uploaded_image.processed_image.name = os.path.join('debug', processed_image_name)
#                     uploaded_image.save()
                
#                 # Формируем контекст для шаблона
#                 context = {
#                     'uploaded_image': uploaded_image,
#                     'detections': detections,
#                     # Используем .url для получения полного URL изображения
#                     'classification_results': classification_results,
#                     'processed_image_url': uploaded_image.processed_image.url
#                 }
                
#                 return render(request, 'core/results.html', context)
            
#             except Exception as e:
#                 error_message = f"Ошибка при обработке изображения: {str(e)}"
#                 return render(request, 'core/error.html', {'message': error_message})
    
#     else:
#         form = ImageUploadForm()
    
#     return render(request, 'core/upload.html', {'form': form})