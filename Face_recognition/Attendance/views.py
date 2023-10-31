from django.shortcuts import render
from .forms import ImageUploadForm

def home(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded image here
            uploaded_image = form.cleaned_data['Image']
            # Call your face recognition code on 'uploaded_image'
    else:
        form = ImageUploadForm()

    return render(request, 'upload_image.html', {'form': form})


# Create your views here.
def home(request):

    return render(request,'home.html')