from django.shortcuts import render,redirect,HttpResponse
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Student,attendance
from .forms import ImageUploadForm
import csv
import face_recognition as fr
import os
import cv2

# imgs=os.listdir('imgs/')
# for img in imgs:
#     roll='22000'+os.path.splitext(img)[0]
#     pas=roll
#     user=User.objects.create(username=roll,password=pas)
#     name=roll
#     stu=Student.objects.create(user=user,Name=name,Photo=img)
#     stu.save()



# attendance={}
# with open('att.csv','r+') as f:
#     names=f.readlines()

#     for line in names:
#         Name=line.split(',')
#         attendance[Name[0]]=0

def encode_faces(folder):
    list_people_encoding=[]
    for filename in os.listdir(folder):
        known_image=fr.load_image_file(f'{folder}{filename}')
        if len(known_image)>0:
         know_encoding=fr.face_encodings(known_image)[0]
         list_people_encoding.append((know_encoding,os.path.splitext(filename)[0]))
    return list_people_encoding

encoded_faces=encode_faces('imgs/')
def find_target_face(target_images,target_encodings,date,course):
    face_location=fr.face_locations(target_images)
    for person in encoded_faces:
        encoded_face=person[0]
        filename=person[1]
        is_target_face=fr.compare_faces(encoded_face, target_encodings,tolerance=0.48)

        if face_location:
            face_number =0
            for location in face_location:
                if is_target_face[face_number]:
                    label = filename
                    markAttendance(label,date,course)
                face_number+=1

def markAttendance (label,date,course):
    name='22000'+label
    stu=Student.objects.filter(user=User.objects.filter(username=name)[0])[0]
    att=1
    if attendance.objects.filter(student=stu,attendance=att,date=date,course=course).exists():
        return
    atten=attendance.objects.create(student=stu,attendance=att,date=date,course=course)
    atten.save()
    # if attendance[os.path.splitext(label)[0]]==0:
    #     attendance[os.path.splitext(label)[0]]+=1



# with open('att.csv', 'r') as f:
#     reader = csv.reader(f)
#     rows = list(reader)

# for row in rows:
#     row.append(attendance[row[0]])

# with open('att.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerows(rows)

print('done')
def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                photos = request.FILES.getlist('Image')  # Access the list of uploaded files
                date=request.POST.get('date')
                course=request.POST.get('course')
                for photo in photos:

                        # Save the photo to the 'uploads' folder
                    with open(os.path.join(settings.MEDIA_ROOT, 'uploads', photo.name), 'wb') as destination:
                        for chunk in photo.chunks():
                            destination.write(chunk)
                for file in os.listdir('media/uploads'):
                    img=fr.load_image_file(f'media/uploads/{file}')
                    t_img=fr.face_encodings(img)
                    find_target_face(img,t_img,date,course)
                for photo in photos:

                    file_name=os.path.join(settings.MEDIA_ROOT, 'uploads', photo.name)
                    if os.path.isfile(file_name):
                        os.remove(file_name)
               
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
