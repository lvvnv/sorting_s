// frontend/src/pages/DetectionResultPage.js
import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const DetectionResultPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  // Получаем данные из состояния навигации
  const { image, result } = location.state || {};
  const detections = result?.detections || [];
  const processedImageUrl = result?.processed_image_url;
  
  // Если данных нет, перенаправляем на страницу загрузки
  if (!image || !detections || detections.length === 0) {
    navigate('/detect');
    return null;
  }

  // Функция определения класса уверенности
  const getConfidenceClass = (confidence) => {
    if (confidence > 0.7) return 'bg-success';
    if (confidence > 0.4) return 'bg-warning text-dark';
    return 'bg-danger';
  };

  return (
    <div className="container mt-4 detection-result-page">
      <h2 className="mb-4">Результаты детекции</h2>
      
      <div className="row">
        <div className="col-md-6 mb-3">
          <h4>Оригинальное изображение</h4>
          <img 
            src={image} 
            className="img-fluid rounded shadow" 
            alt="Uploaded Image" 
          />
        </div>
        {processedImageUrl && (
          <div className="col-md-6 mb-3">
            <h4>Обработанное изображение</h4>
            <img 
              src={processedImageUrl} 
              className="img-fluid rounded shadow" 
              alt="Processed Image" 
            />
          </div>
        )}
      </div>

      {/* Мобильное представление */}
      <div className="d-md-none mt-3">
        <h4>Обнаруженные объекты</h4>
        {detections.map((detection, index) => (
          <div key={index} className="card mb-2">
            <div className="card-body">
              <div className="row">
                <div className="col-6">
                  <strong>Класс:</strong> {detection.class}<br />
                  <strong>Уверенность:</strong>
                  <span className={`badge ${getConfidenceClass(detection.confidence)}`}>
                    {(detection.confidence * 100).toFixed(2)}%
                  </span>
                </div>
                <div className="col-6">
                  <strong>Координаты:</strong><br />
                  ({detection.box[0]}, {detection.box[1]})<br />
                  ({detection.box[2]}, {detection.box[3]})
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {/* Десктопное представление */}
      <div className="d-none d-md-block mt-4">
        <h4>Обнаруженные объекты</h4>
        <div className="table-responsive">
          <table className="table table-striped table-hover">
            <thead className="table-light">
              <tr>
                <th>Класс</th>
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
          onClick={() => navigate('/detect')} 
          className="btn btn-primary btn-lg"
        >
          <i className="bi bi-arrow-repeat"></i> Загрузить новое изображение
        </button>
      </div>
    </div>
  );
};

export default DetectionResultPage;
