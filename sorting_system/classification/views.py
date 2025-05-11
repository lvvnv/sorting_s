import requests
from django.shortcuts import render
from .forms import ImageUploadForm

def classify_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['image']
            # Вызов внешнего API модели
            files = {'file': image.read()}
            response = requests.post('http://localhost:5000/classify', files=files)
            result = response.json()
            return render(request, 'classification/result.html', {'result': result})
    else:
        form = ImageUploadForm()
    return render(request, 'classification/upload.html', {'form': form})