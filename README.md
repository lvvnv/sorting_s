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
