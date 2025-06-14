import numpy as np
import cv2
import logging
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.models import Model

logger = logging.getLogger(__name__)

# Загрузка модели при старте приложения
model = None
class_names = ['plastic', 'glass', 'paper', 'metal']  # Пример классов

def load_classifier_model():
    global model
    if model is None:
        try:
            # Создаем модель EfficientNetB0 с кастомной головой
            base_model = EfficientNetB0(
                weights='imagenet', 
                include_top=False, 
                input_shape=(224, 224, 3))
            
            # Добавляем кастомные слои
            x = base_model.output
            x = GlobalAveragePooling2D()(x)
            predictions = Dense(len(class_names), activation='softmax')(x)
            
            # Собираем модель
            model = Model(inputs=base_model.input, outputs=predictions)
            
            # Замораживаем базовые слои
            for layer in base_model.layers:
                layer.trainable = False
                
            logger.info("Модель EfficientNetB0 успешно создана")
        except Exception as e:
            logger.error(f"Ошибка создания модели: {str(e)}")
            raise
    return model

def preprocess_image(image):
    try:
        # Конвертируем в RGB (OpenCV использует BGR по умолчанию)
        if len(image.shape) == 2:  # Если изображение в градациях серого
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Изменение размера и предобработка
        image = cv2.resize(image, (224, 224))
        image = preprocess_input(image)
        return np.expand_dims(image, axis=0)
    except Exception as e:
        logger.error(f"Ошибка предобработки изображения: {str(e)}")
        raise

def classify_waste(image):
    try:
        classifier = load_classifier_model()
        processed = preprocess_image(image)
        
        # Для демонстрации - случайный результат
        # В реальном приложении нужно использовать обученную модель
        class_idx = np.random.randint(0, len(class_names))
        confidence = np.random.uniform(0.7, 0.95)
        
        return class_names[class_idx], float(confidence)
    except Exception as e:
        logger.error(f"Ошибка классификации: {str(e)}")
        return "unknown", 0.0