// frontend/src/pages/UploadPage.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { classifyImage } from '../services/classificationService';

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type.startsWith('image/')) {
      setFile(selectedFile);
      setError('');
    } else {
      setError('Пожалуйста, выберите изображение (JPG, PNG и т.д.)');
      setFile(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Пожалуйста, выберите изображение');
      return;
    }
    
    setIsLoading(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('image', file);
      
      const response = await classifyImage(formData);
      
      // Перенаправляем на страницу результатов
      navigate('/results', { 
        state: { 
          result: response.data,
          image: URL.createObjectURL(file)
        } 
      });
    } catch (err) {
      console.error('Error during classification:', err);
      
      let errorMessage = 'Ошибка при обработке изображения';
      if (err.response?.data?.error) {
        errorMessage = err.response.data.error;
      } else if (err.message.includes('413')) {
        errorMessage = 'Изображение слишком большое';
      }
      
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="card-header bg-primary text-white">
        <h2>Загрузите изображение для анализа</h2>
      </div>
      <div className="card-body">
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="image" className="form-label">
              Выберите изображение:
            </label>
            <input
              type="file"
              id="image"
              className="form-control"
              accept="image/*"
              onChange={handleFileChange}
              disabled={isLoading}
            />
            {file && (
              <div className="mt-2">
                <img 
                  src={URL.createObjectURL(file)} 
                  alt="Preview" 
                  className="img-thumbnail" 
                  style={{ maxWidth: '200px' }} 
                />
              </div>
            )}
          </div>
          
          {error && (
            <div className="alert alert-danger" role="alert">
              {error}
            </div>
          )}
          
          <button 
            type="submit" 
            className="btn btn-success btn-lg w-100"
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Анализируем...
              </>
            ) : (
              'Анализировать'
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default UploadPage;
