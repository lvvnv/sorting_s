// frontend/src/pages/AboutPage.js
import React from 'react';

const AboutPage = () => {
  return (
    <div className="about-page">
      <h2>Цель проекта</h2>
      <p>
        Разработка сервиса по автоматической классификации и детекции отходов на изображениях{' '}
        <a 
          href="https://github.com/IrinaGoloshchapova/ml_system_design_doc_ru" 
          target="_blank" 
          rel="noopener noreferrer"
        >
          [1]
        </a>.
      </p>
    </div>
  );
};

export default AboutPage;
