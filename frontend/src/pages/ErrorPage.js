// frontend/src/pages/ErrorPage.js
import React from 'react';
import { useLocation, Link } from 'react-router-dom';

const ErrorPage = () => {
  const location = useLocation();
  const message = location.state?.message || "Неизвестная ошибка";
  
  return (
    <div className="error-page">
      <div className="alert alert-danger" role="alert">
        <h4 className="alert-heading">Ошибка!</h4>
        <p>{message}</p>
        <hr />
        <p className="mb-0">Попробуйте загрузить другое изображение или обратитесь к администратору.</p>
      </div>
      <div className="text-center mt-4">
        <Link to="/classify" className="btn btn-primary">
          Попробовать снова
        </Link>
      </div>
    </div>
  );
};

export default ErrorPage;
