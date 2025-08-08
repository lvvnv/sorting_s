// frontend/src/pages/ResultsPage.js
import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  // Получаем данные из состояния навигации
  const { originalImage, processedImage, detections } = location.state || {};
  
  // Если данных нет, перенаправляем на страницу загрузки
  if (!originalImage || !processedImage || !detections) {
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
    <div className="container mt-4 results-page">
      <h2 className="mb-4">Результаты анализа</h2>
      
      <div className="row">
        <div className="col-md-6 mb-3">
          <h4>Оригинальное изображение</h4>
          <img 
            src={originalImage} 
            className="img-fluid rounded shadow" 
            alt="Uploaded Image" 
          />
        </div>
        <div className="col-md-6 mb-3">
          <h4>Обработанное изображение</h4>
          <img 
            src={processedImage} 
            className="img-fluid rounded shadow" 
            alt="Processed Image" 
          />
        </div>
      </div>

      {/* Мобильное представление (скрыто на десктопе) */}
      <div className="d-md-none mt-3">
        <h4>Обнаруженные объекты</h4>
        {detections.map((detection, index) => (
          <div key={index} className="card mb-2">
            <div className="card-body">
              <div className="row">
                <div className="col-6">
                  <strong>Детекция:</strong> {detection.class}<br />
                  <strong>Уверенность:</strong>
                  <span className={`badge ${getConfidenceClass(detection.confidence)}`}>
                    {(detection.confidence * 100).toFixed(2)}%
                  </span>
                </div>
                <div className="col-6">
                  <strong>Классификация:</strong> {detection.classification_class}<br />
                  <strong>Уверенность:</strong>
                  <span className={`badge ${getConfidenceClass(detection.classification_confidence)}`}>
                    {(detection.classification_confidence * 100).toFixed(2)}%
                  </span>
                </div>
              </div>
              <div className="mt-2">
                <strong>Координаты:</strong><br />
                ({detection.box[0]}, {detection.box[1]})<br />
                ({detection.box[2]}, {detection.box[3]})
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {/* Десктопное представление (скрыто на мобильных) */}
      <div className="d-none d-md-block mt-4">
        <h4>Обнаруженные объекты</h4>
        <div className="table-responsive">
          <table className="table table-striped table-hover">
            <thead className="table-light">
              <tr>
                <th>Класс (Детекция)</th>
                <th>Уверенность</th>
                <th>Класс (Классификация)</th>
                <th>Уверенность</th>
                <th>Координаты</th>
              </tr>
            </thead>
            <tbody>
              {detections.map((detection, index) => (
                <tr key={index}>
                  <td>{detection.class}</td>
                  <td>
                    <span className={`badge ${getConfidenceClass(detection.confidence)}`}>
                      {(detection.confidence * 100).toFixed(2)}%
                    </span>
                  </td>
                  <td>{detection.classification_class}</td>
                  <td>
                    <span className={`badge ${getConfidenceClass(detection.classification_confidence)}`}>
                      {(detection.classification_confidence * 100).toFixed(2)}%
                    </span>
                  </td>
                  <td>
                    <small>
                      ({detection.box[0]}, {detection.box[1]})<br />
                      ({detection.box[2]}, {detection.box[3]})
                    </small>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      
      <div className="mt-4 text-center">
        <button 
          onClick={() => navigate('/classify')} 
          className="btn btn-primary btn-lg"
        >
          <i className="bi bi-arrow-repeat"></i> Загрузить новое изображение
        </button>
      </div>
    </div>
  );
};

export default ResultsPage;
