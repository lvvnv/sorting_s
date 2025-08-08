// frontend/src/services/detectionService.js
import axios from 'axios';

const api = axios.create({
  baseURL: '/api/',
  headers: {
    'Content-Type': 'application/json',
  }
});

// Получаем CSRF-токен для Django
const getCSRFToken = () => {
  return document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;
};

// API для обработки изображения
export const processImage = async (formData) => {
  return api.post('process/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      'X-CSRFToken': getCSRFToken()
    }
  });
};
