from django import forms
from models import UserModel,PostModel

class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields=['email', 'name', 'username','password']


class LoginForm(forms.ModelForm):
    class Meta:
        model= UserModel
        fields= ['username', 'password']

class PostForm(forms.ModelForm):
    class Meta:
      model=PostModel
      fields=['image', 'caption']