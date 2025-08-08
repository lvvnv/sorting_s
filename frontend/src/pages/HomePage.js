// frontend/src/pages/HomePage.js
import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div className="home-page">
      <h1>Добро пожаловать в сервис по классификации отходов</h1>
      <p>Загрузите фото и узнайте тип мусора.</p>
      <Link to="/classify" className="btn btn-primary">
        Начать
      </Link>
    </div>
  );
};

export default HomePage;
