// frontend/src/pages/NoDetectionsPage.js
import React from 'react';
import { Link } from 'react-router-dom';

const NoDetectionsPage = () => {
  return (
    <div className="no-detections-page">
      <div className="alert alert-warning" role="alert">
        <h4 className="alert-heading">Объекты не обнаружены!</h4>
        <p>На загруженном изображении не было обнаружено объектов мусора.</p>
        <hr />
        <p className="mb-0">Попробуйте загрузить другое изображение с более четкими объектами.</p>
      </div>
      <div className="text-center mt-4">
        <Link to="/classify" className="btn btn-primary">
          Загрузить другое изображение
        </Link>
      </div>
    </div>
  );
};

export default NoDetectionsPage;
