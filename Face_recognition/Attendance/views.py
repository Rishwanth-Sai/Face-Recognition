from django.shortcuts import render,redirect,HttpResponse
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Student
from .forms import ImageUploadForm

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                photos = request.FILES.getlist('Image')  # Access the list of uploaded files

                for photo in photos:

                        # Save the photo to the 'uploads' folder
                    with open(os.path.join(settings.MEDIA_ROOT, 'uploads', photo.name), 'wb') as destination:
                        for chunk in photo.chunks():
                            destination.write(chunk)

                return redirect('view_photos')

            return render(request, 'home.html')
        return render(request,'courses.html')
    return redirect('login')
def Login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        role=request.POST.get('role')
        if role=='student':
            user=authenticate(request,username=username,password=password)
            if user is not None:
                if user.is_staff:
                    return render(request,'login.html')
                login(request,user)
                return redirect('home')
            return render(request,'login.html')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('home')
            return render(request,'login.html')
        return render(request,'login.html')
    if request.user.is_authenticated:
        logout(request)
    return render(request,'login.html')

def view_photos(request):
    photos_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    photo_files = os.listdir(photos_dir)
    photo_urls = [os.path.join(settings.MEDIA_URL, 'uploads', photo) for photo in photo_files]

    return render(request, 'photos.html', {'photo_urls': photo_urls})

def signup(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pas1=request.POST.get('password1')
        pas2=request.POST.get('password2')
        name=request.POST.get('name')        
        photo=request.FILES.get('Image')
        if(pas1==pas2):
            user=User.objects.create(username=username,password=pas1)
            user.save()
            student=Student.objects.create(user=user,Name=name,photo=photo)
            student.save()
            user2=authenticate(request,username=username,password=pas1)
            if user2 is not None:
                login(request,user2)
                return redirect('home')

    return render(request,'signup.html')

def courses(request):
    return render(request,'courses.html')

def edit(request):
    return render(request,'edit.html')
# Create your views here.
