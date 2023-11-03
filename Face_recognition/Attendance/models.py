from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Name=models.CharField(max_length=50)
    Photo=models.ImageField()

class attendance(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    attendance=models.BooleanField(default=0)
    date=models.DateField()
    course=models.CharField(default='DSA',max_length=50)
