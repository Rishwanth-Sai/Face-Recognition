from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    user=User.models.ForeignKey(on_delete=models.CASCADE)
    Name=models.CharField(max_length=50)
    Photo=models.ImageField()
    