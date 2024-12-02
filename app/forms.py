from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Wrapped

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        
class WrappedForm(forms.ModelForm):
    class Meta:
        model = Wrapped
        fields = ['data', 'public']
        widgets = {
            'data': forms.HiddenInput(),
            'public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
