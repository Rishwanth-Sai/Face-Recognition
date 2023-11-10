from django.shortcuts import render,redirect,HttpResponse
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from .models import Student,attendance
from .forms import ImageUploadForm
import csv
import face_recognition as fr
import os

# imgs=os.listdir('imgs/')
# for img in imgs:
#     roll='22000'+os.path.splitext(img)[0]
#     pas=roll
#     user=User.objects.create(username=roll,password=make_password(pas))
#     name=roll
#     stu=Student.objects.create(user=user,Name=name,Photo=img)
#     stu.save()


print("THIS MAY TAKE A WHILE TO ENCODE DATABASE FACES AND GENERATE LINK")

attendances={}
def attend():
    with open('Attendance/templates/attendance.csv','r+') as f:
        names=csv.reader(f)
        next(names)
        for line in names:
            
            attendances[line[0]]=0
    return

def encode_faces():
    list_people_encoding=[]
    pupil=Student.objects.all()
    for filename in pupil:
        known_image=fr.load_image_file(filename.Photo)
        if len(known_image)>0:
         know_encoding=fr.face_encodings(known_image)[0]
         list_people_encoding.append((know_encoding,filename.user.username))
    return list_people_encoding

encoded_faces=encode_faces()
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
    name=label
    stu=Student.objects.filter(user=User.objects.filter(username=name)[0])[0]
    att=1
    if attendance.objects.filter(student=stu,attendance=att,date=date,course=course).exists():
        return
    atten=attendance.objects.create(student=stu,attendance=att,date=date,course=course)
    atten.save()
    if attendances[name]==0:
        attendances[name]+=1

def writecsv(date):
    with open('Attendance/templates/attendance.csv', 'r') as f:
        reader = csv.reader(f)
        reader=list(reader)
        heading=reader[0]
        rows = reader[1:]
    heading.append(date)
    for row in rows:
        row.append(attendances[row[0]])

    with open('Attendance/templates/attendance.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(heading)
        writer.writerows(rows)

print('done')
def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                photos = request.FILES.getlist('Image')  # Access the list of uploaded files
                date=request.POST.get('date')
                course='DSA'
                if attendance.objects.filter(date=date,course=course).exists():
                    return render(request,'home.html',context={'mssg':'The attendance with this date and course already exists'})
                for photo in photos:

                        # Save the photo to the 'uploads' folder
                    with open(os.path.join(settings.MEDIA_ROOT, 'uploads', photo.name), 'wb') as destination:
                        for chunk in photo.chunks():
                            destination.write(chunk)
                attend()
                for file in os.listdir('media/uploads'):
                    img=fr.load_image_file(f'media/uploads/{file}')
                    t_img=fr.face_encodings(img)
                    find_target_face(img,t_img,date,course)
                writecsv(date)
                for photo in photos:

                    file_name=os.path.join(settings.MEDIA_ROOT, 'uploads', photo.name)
                    if os.path.isfile(file_name):
                        os.remove(file_name)
               
                return redirect('courses')

            return render(request, 'home.html',context={'mssg':''})
        stu=Student.objects.filter(user=request.user)[0]
        return render(request,'profile.html',context={'student':stu})
    return redirect('login')
def Login(request):
    context={'mssg':''}
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        role=request.POST.get('role')
        if role=='student':
            user=authenticate(request,username=username,password=password)
            if user is not None:
                if user.is_staff:
                    context['mssg']='Wrong credentials'
                    return render(request,'login.html',context)
                login(request,user)
                return redirect('home')
            context['mssg']='Wrong credentials'
            return render(request,'login.html',context)
        user=authenticate(request,username=username,password=password)
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('home')
            context['mssg']='Wrong credentials'
            return render(request,'login.html',context)
        context['mssg']='Wrong credentials'
        return render(request,'login.html',context)
    if request.user.is_authenticated:
        logout(request)
    return render(request,'login.html',context)

def download_csv(request):
    with open('Attendance/templates/attendance.csv', 'r') as f:
        reader = csv.reader(f)
        reader=list(reader)    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'
    writer = csv.writer(response)
    for row in reader:
        writer.writerow(row)
    return response
def download_csv_stu(request):
    with open('Attendance/templates/attendance.csv', 'r') as f:
        reader = csv.reader(f)
        reader=list(reader)    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'
    writer = csv.writer(response)
    for row in reader:
        if row[0]=='Name' or row[0]==request.user.username:
            writer.writerow(row)
    return response
def signup(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pas1=request.POST.get('password1')
        pas2=request.POST.get('password2')
        name=request.POST.get('name')        
        photo=request.FILES.get('Image')
        if User.objects.filter(username=username).exists():
            return render(request,'signup.html',context={'mssg':'This user already exists'})
        if(pas1==pas2):
            if os.path.splitext(photo.name)[0]==username[-4:]:
                user=User.objects.create(username=username,password=make_password(pas1))
                user.save()
                student=Student.objects.create(user=user,Name=name,Photo=photo)
                student.save()
                user2=authenticate(request,username=username,password=pas1)
                with open('Attendance/templates/attendance.csv', 'r') as f:
                    reader = csv.reader(f)
                    reader=list(reader)
                    size=len(reader[0])
                    row=[username]
                for i in range(1,size):
                    row.append(0)

                with open('Attendance/templates/attendance.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(reader)
                    writer.writerow(row)
                if user2 is not None:
                    login(request,user2)
                    return redirect('home')
            return render(request,'signup.html',context={'mssg':'Give the photo file name same as last 4 digits of the roll number.'})
        return render(request,'signup.html',context={'mssg':'Check the passwords.'})
    return render(request,'signup.html',context={'mssg':''})

def courses(request):
    stu=len(Student.objects.all())
    att=attendance.objects.values('date').distinct().count()
    if att==0:
        att+=1
    attper=len(attendance.objects.filter(course='DSA'))
    attper/=stu*att
    attper*=100
    attper=f"{attper:.{3}f}"
    return render(request,'courses.html',context={'att':attper,'stu':stu})

def edit(request):
    if request.method=='POST':
        roll2=request.POST.get('roll_numbers')
        course=request.POST.get('course')
        date=request.POST.get('date')
        attend=request.POST.get('attendance')
        roll=roll2.split()
        for num in roll:
            if User.objects.filter(username=num).exists()==0:
                return render(request,'edit.html',context={'mssg':'Check the rollnumbers'})
        if attendance.objects.filter(date=date,course=course).exists():
            for num in roll:
                if(attend=='present'):
                    val=1
                    if attendance.objects.filter(student=Student.objects.filter(user=User.objects.filter(username=num)[0])[0],date=date,course=course).exists()==0:
                        att=attendance.objects.create(student=Student.objects.filter(user=User.objects.filter(username=num)[0])[0],date=date,course=course,attendance=1)
                        att.save()
                else:
                    val=0
                    if attendance.objects.filter(student=Student.objects.filter(user=User.objects.filter(username=num)[0])[0],date=date,course=course).exists():
                        att2=attendance.objects.filter(student=Student.objects.filter(user=User.objects.filter(username=num)[0])[0],date=date,course=course)[0]
                        att2.attendance=0  
                with open('Attendance/templates/attendance.csv', 'r') as f:
                    reader = csv.reader(f)
                    reader=list(reader)
            k=-1
            l=-1
            for num in roll:
                for i in range(0,len(reader[0])):
                    if reader[0][i]==date:
                        k=i        
                for i in range(0,len(reader)):
                    if reader[i][0]==num:
                        l=i   
                reader[l][k]=val  
            with open('Attendance/templates/attendance.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(reader) 
            return render(request,'edit.html',context={'mssg':'Your attendance has been changed.'})
        return render(request,'edit.html',context={'mssg':'The attendance for this date doesnot exist.'})
    return render(request,'edit.html',context={'mssg':''})

def courses2(request):
    att=attendance.objects.values('date').distinct().count()
    if att==0:
        att+=1
    stu=len(attendance.objects.filter(student=Student.objects.filter(user=request.user)[0],course='DSA'))
    attper=stu/att
    attper*=100
    return render(request,'courses2.html',context={'attper':attper,'att':att,'stu':stu})