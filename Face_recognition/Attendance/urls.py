from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("courses", views.courses, name="courses"),
    path("edit", views.edit, name="edit"),  
    path("login", views.Login, name="login"),  
    path("signup", views.signup, name="signup"), 
    path('photos/', views.view_photos, name='view_photos'), 

]