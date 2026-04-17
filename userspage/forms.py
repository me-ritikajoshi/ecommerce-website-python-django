from typing import Any
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username=forms.CharField(max_length=150, strip=True)
    password=forms.CharField(widget=forms.PasswordInput, strip=False)
    
class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email']
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm,self).__init__(*args, **kwargs)
        self.fields.pop('password',None)
        self.fields["email"].required = True
        self.fields["first_name"].required = True
        
