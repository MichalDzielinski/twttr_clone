from django import forms
from .models import Meep, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label='Profile Picture', required=False)

    class Meta:
        model = Profile 
        fields = ('profile_image',)

class MeepForm(forms.ModelForm):
    body = forms.CharField(required=True, 
                           widget=forms.widgets.Textarea(
                               attrs={
                                   'placeholder': 'Enter Your Musker Meep!',
                                   'class': 'form-control',
                               }
                           ), label='',)
    class Meta:
        model = Meep
        exclude = ('user', 'likes' )
 
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Email Address"}))
    first_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "First Name"}))
    last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Last Name"}))


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = ""

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = ""
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'repeat password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text ="" 

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "User name"}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Email Address"}))
    first_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "First Name"}))
    last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Last Name"}))

    password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "password"}))
    password2 = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "repeat password"}))

    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2')

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError('Passwords dont match')
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user

   