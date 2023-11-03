from django import forms

class ImageUploadForm(forms.Form):
    date=forms.DateField()
    Course=forms.CharField(max_length=50)
    image = forms.ImageField()

