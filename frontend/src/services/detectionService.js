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

// API для детекции
export const detectObjects = async (formData) => {
  console.log("Calling detectObjects service");
  return api.post('detect/', formData, {
    headers: {
      'X-CSRFToken': getCSRFToken()
    }
  });
};
