from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from account.models import Profile

User = get_user_model()

class RegistrationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('email','user_name','password1','password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('user',)