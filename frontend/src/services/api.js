import axios from 'axios';

const api = axios.create({
  baseURL: '/api/', // Базовый URL для API
  headers: {
    'Content-Type': 'application/json',
  }
});

// Добавляем CSRF-токен для Django
api.interceptors.request.use(config => {
  const token = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
  if (token) {
    config.headers['X-CSRFToken'] = token;
  }
  return config;
});

// API для классификации
export default {
  classifyImage: (formData) => api.post('classify/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }),
  detectImage: (formData) => api.post('detect/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }),
};
