// frontend/src/pages/ClassificationResultPage.js
import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const ClassificationResultPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const result = location.state?.result;
  
  if (!result) {
    return (
      <div className="classification-result-page">
        <h2>Результат классификации</h2>
        <p>Нет данных о результате. Пожалуйста, загрузите изображение для классификации.</p>
        <button 
          onClick={() => navigate('/classify')} 
          className="btn btn-primary"
        >
          Загрузить изображение
        </button>
      </div>
    );
  }

  return (
    <div className="classification-result-page">
      <h2>Результат классификации</h2>
      <ul className="result-list">
        <li><strong>Категория:</strong> {result.class_name}</li>
        <li><strong>Уверенность:</strong> {parseFloat(result.confidence).toFixed(2) * 100}%</li>
      </ul>
      <button 
        onClick={() => navigate('/classify')} 
        className="btn btn-secondary"
      >
        Загрузить другое изображение
      </button>
    </div>
  );
};

export default ClassificationResultPage;
