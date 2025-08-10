// frontend/src/pages/ClassificationResultPage.js
import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const ClassificationResultPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { result, image } = location.state || {};
  
  // Если данных нет, перенаправляем на страницу загрузки
  if (!result || !image) {
    navigate('/classify');
    return null;
  }

  // Функция определения класса уверенности
  const getConfidenceClass = (confidence) => {
    if (confidence > 0.7) return 'bg-success';
    if (confidence > 0.4) return 'bg-warning text-dark';
    return 'bg-danger';
  };

  return (
    <div className="classification-result-page">
      <h2 className="mb-4">Результат классификации</h2>
      
      <div className="row">
        <div className="col-md-6 mb-4">
          <h4 className="mb-3">Ваше изображение</h4>
          <div className="image-preview-container" style={{ 
            border: '1px solid #dee2e6',
            borderRadius: '8px',
            padding: '10px',
            backgroundColor: '#fff'
          }}>
            <img 
              src={image} 
              className="img-fluid rounded shadow-sm" 
              alt="Загруженное изображение" 
              style={{ 
                maxWidth: '100%',
                height: 'auto',
                borderRadius: '5px'
              }}
            />
          </div>
        </div>
        
        <div className="col-md-6 mb-4">
          <h4 className="mb-3">Результат анализа</h4>
          <div className="result-card p-4" style={{ 
            backgroundColor: '#fff',
            borderRadius: '8px',
            boxShadow: '0 4px 6px rgba(0,0,0,0.05)',
            border: '1px solid #dee2e6'
          }}>
            <div className="result-item mb-3">
              <h5 className="text-muted">Определенный тип:</h5>
              <div className="d-flex align-items-center">
                <i className="bi bi-tag-fill me-2" style={{ color: '#0d6efd' }}></i>
                <span className="fs-4 fw-bold text-capitalize">{result.class_name}</span>
              </div>
            </div>
            
            <div className="result-item">
              <h5 className="text-muted">Уверенность определения:</h5>
              <div className="d-flex align-items-center mt-2">
                <div className="progress w-100" style={{ height: '20px' }}>
                  <div 
                    className={`progress-bar ${getConfidenceClass(result.confidence)}`}
                    role="progressbar" 
                    style={{ width: `${result.confidence * 100}%` }}
                  >
                    {(result.confidence * 100).toFixed(1)}%
                  </div>
                </div>
              </div>
              <div className="mt-3">
                <span className="badge rounded-pill px-3 py-2" style={{ 
                  fontSize: '1rem',
                  backgroundColor: 'var(--bs-gray-100)'
                }}>
                  <i className="bi bi-info-circle me-1"></i>
                  {result.confidence > 0.7 ? "Высокая уверенность" : 
                   result.confidence > 0.4 ? "Средняя уверенность" : "Низкая уверенность"}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="mt-4 p-3 bg-light rounded">
        <h5 className="mb-3">Рекомендации по утилизации</h5>
        <div className="recommendations">
          {result.class_name === 'plastic' && (
            <div>
              <h6>Пластик</h6>
              <p>Пластиковые отходы следует сортировать по типам пластика. Убедитесь, что упаковка чистая и сухая перед утилизацией.</p>
            </div>
          )}
          
          {result.class_name === 'glass' && (
            <div>
              <h6>Стекло</h6>
              <p>Стеклянная тара должна быть чистой и снятой крышкой. Разные цвета стекла сортируются отдельно.</p>
            </div>
          )}
          
          {result.class_name === 'metal' && (
            <div>
              <h6>Металл</h6>
              <p>Металлические банки и упаковку следует промыть и сплющить для экономии места при утилизации.</p>
            </div>
          )}
          
          {result.class_name === 'paper' && (
            <div>
              <h6>Бумага</h6>
              <p>Бумажные отходы должны быть сухими и чистыми. Упаковка из-под молока и других продуктов не подходит для переработки.</p>
            </div>
          )}
          
          {result.class_name === 'cardboard' && (
            <div>
              <h6>Картон</h6>
              <p>Картон следует сложить и упаковать в компактный блок. Убедитесь, что картон не загрязнен жиром или влагой.</p>
            </div>
          )}
          
          {result.class_name === 'trash' && (
            <div>
              <h6>Смешанные отходы</h6>
              <p>К сожалению, система не смогла определить тип отходов с достаточной уверенностью. Рекомендуется поместить этот предмет в общий контейнер для отходов.</p>
            </div>
          )}
        </div>
      </div>
      
      <div className="mt-4 d-flex justify-content-between">        
        <button 
          onClick={() => navigate('/classify')} 
          className="btn btn-primary"
        >
          <i className="bi bi-arrow-repeat me-2"></i>Загрузить другое изображение
        </button>
      </div>
    </div>
  );
};

export default ClassificationResultPage;