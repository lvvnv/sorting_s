import cv2
import numpy as np
import os
import logging
import random
from ultralytics import YOLO
from django.conf import settings
from classification.classifier import classify_waste  # Импорт классификатора

logger = logging.getLogger(__name__)

# Загрузка модели при старте приложения
model = None

def load_model():
    global model
    if model is None:
        try:
            model_path = 'detection/weights/best_1.pt'
            if not os.path.exists(model_path):
                logger.info("Downloading YOLOv8 model...")
                import gdown
                url = 'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt'
                os.makedirs(os.path.dirname(model_path), exist_ok=True)
                gdown.download(url, model_path, quiet=False)
            
            model = YOLO(model_path)
            logger.info("YOLOv8 model loaded successfully")
        except Exception as e:
            logger.error(f"Model loading error: {str(e)}")
            raise
    return model

def detect_objects(image_path):
    try:
        detector = load_model()
        img = cv2.imread(image_path)
        
        if img is None:
            raise ValueError(f"Could not read image at {image_path}")
        
        # Конвертируем в RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Выполняем детекцию
        results = detector(img_rgb, conf=0.25)
        
        detections = []
        
        # Обрабатываем результаты
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy().astype(int)
            class_names = result.names
            
            for i in range(len(boxes)):
                x_min, y_min, x_max, y_max = map(int, boxes[i])
                confidence = float(confidences[i])
                class_id = int(class_ids[i])
                class_name = class_names.get(class_id, f"class_{class_id}")
                
                # Вырезаем ROI для классификации
                roi = img[y_min:y_max, x_min:x_max]
                
                # Пропускаем слишком маленькие области
                if roi.size == 0 or min(roi.shape[:2]) < 5:
                    continue
                
                # Определяем материал с помощью классификатора
                material, material_confidence = classify_waste(roi)
                
                # Генерируем случайный цвет
                color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
                
                detections.append({
                    'x_min': x_min,
                    'y_min': y_min,
                    'x_max': x_max,
                    'y_max': y_max,
                    'confidence': confidence,
                    'class_id': class_id,
                    'class_name': class_name,
                    'material': material,
                    'material_confidence': material_confidence,
                    'roi': roi,
                    'color': color
                })
        
        logger.info(f"Detected {len(detections)} objects")
        
        # Создаем изображение с bounding boxes
        debug_img = img.copy()
        for det in detections:
            cv2.rectangle(
                debug_img, 
                (det['x_min'], det['y_min']), 
                (det['x_max'], det['y_max']), 
                det['color'], 2
            )
            
            label = f"{det['class_name']} | {det['material']} {det['material_confidence']:.2f}"
            cv2.putText(
                debug_img, 
                label, 
                (det['x_min'], det['y_min'] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, 
                det['color'], 
                2
            )
        
        # Сохраняем отладочное изображение
        debug_dir = os.path.join(settings.MEDIA_ROOT, 'debug')
        os.makedirs(debug_dir, exist_ok=True)
        
        debug_filename = f"det_{os.path.basename(image_path)}"
        debug_path = os.path.join(debug_dir, debug_filename)
        cv2.imwrite(debug_path, debug_img)
        
        logger.info(f"Detection debug image saved to: {debug_path}")
        
        # Добавляем URL отладочного изображения
        for det in detections:
            det['debug_url'] = os.path.join(
                settings.MEDIA_URL, 
                'debug', 
                debug_filename
            )
        
        return detections
    
    except Exception as e:
        logger.error(f"Detection error: {str(e)}", exc_info=True)
        raise

def detect_waste(image_path):
    return detect_objects(image_path)