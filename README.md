# sorting_s

```
sorting_system/
├── api/ - REST API для энсемблирования моделей
│   ├── __init__.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── classification/ - приложение для классификации
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py         
│   ├── views.py
│   ├── urls.py           
│   └── classifier.py     
├── core/ - общая логика
│   ├── __init__.py
│   ├── models.py
│   └── views.py
├── detection/ - приложение для детекции
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py         
│   ├── urls.py           
│   └── detector.py       
├── monitoring/ - инструменты мониторинга
│   ├── __init__.py
│   ├── metrics.py
│   └── middleware.py
├── sorting_system/       
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py          
│   └── wsgi.py
├── users/
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py
│   └── views.py
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Docker Usage

To run the application using Docker:

1. Make sure you have Docker installed
2. Run the following command to start the services:
   ```bash
   docker-compose up --build
   ```

3. Access the services:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/
   - Classification endpoint: http://localhost:8000/api/classify/
   - Detection endpoint: http://localhost:8000/api/detect/

4. To stop the services:
   ```bash
   docker-compose down
   ```

5. To rebuild the services:
   ```bash
   docker-compose up --build --force-recreate
   ```

## API Endpoints

The backend provides the following API endpoints:

- `POST /api/classify/` - Upload an image for classification
- `PUT /api/classify/<image_id>/` - Update classification result (mark as wrong)
- `DELETE /api/classify/<image_id>/` - Delete classification result
- `POST /api/detect/` - Upload an image for object detection
- `DELETE /api/detect/<image_id>/` - Delete detection result

## Development

For local development without Docker:

1. Set up a Python virtual environment:
   ```bash
   cd sorting_system
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run database migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

5. In a separate terminal, start the frontend:
   ```bash
   cd frontend
   npm install
   npm start
   ```