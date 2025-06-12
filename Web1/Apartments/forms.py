from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django import forms
from .models import User,Apartment,Image,Request

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username','password1']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','password1','password2', 'phone', 'status','commission']

class AddApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['city', 'street', 'floor', 'rooms','price','description']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['url']

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['content']

    content = forms.CharField(label="הכנס פנייה", required=True)


# class AddApartmentForm():
#     class Meta:
