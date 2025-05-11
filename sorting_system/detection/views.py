import requests
from django.shortcuts import render
from classification.forms import ImageUploadForm

def detect_objects(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['image']
            files = {'file': image.read()}
            response = requests.post('http://localhost:5000/detect', files=files)
            result = response.json()
            return render(request, 'detection/result.html', {'result': result})
    else:
        form = ImageUploadForm()
    return render(request, 'detection/upload.html', {'form': form})