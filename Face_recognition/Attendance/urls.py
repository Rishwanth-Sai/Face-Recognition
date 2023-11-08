from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("courses", views.courses, name="courses"),
    path("edit", views.edit, name="edit"),  
    path("login", views.Login, name="login"),  
    path("signup", views.signup, name="signup"), 
    path("courses2", views.courses2, name="courses2"), 
    path('download_csv', views.download_csv, name='download_csv'), 
    path('download_csv_stu', views.download_csv_stu, name='download_csv_stu'), 

]