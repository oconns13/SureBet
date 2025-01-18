
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input text'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input text'}), max_length=64, help_text='Enter a valid email address')
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise forms.ValidationError("Email already exists")
        return email

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class AuthenticateUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input text'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta():
        model = User
        fields = ('username', 'password')