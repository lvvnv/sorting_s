// frontend/src/services/classificationService.js
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

// API для классификации
export const classifyImage = async (formData) => {
  return api.post('classify/', formData, {
    headers: {
      'X-CSRFToken': getCSRFToken()
    }
  });
};