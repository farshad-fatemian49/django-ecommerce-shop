# from pyexpat import model
# from django import forms
# from django.contrib.auth.forms import UserCreationForm , UserChangeForm
# from .models import CustomUser


# class CustomUserCreationForm(UserCreationForm):
#     model = CustomUser
#     fields = UserCreationForm.Meta.fields + ('age',)
    
# class CustomUserChangeForm(UserChangeForm):
#     model = CustomUser
#     fields = UserChangeForm.Meta.fields


from dataclasses import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=32, help_text='First name')
    # last_name = forms.CharField(max_length=32, help_text='Last name')
    # email = forms.EmailField(max_length=64, help_text='Enter a valid email address')
    

    class Meta(UserCreationForm.Meta):
        model = User
        # I've tried both of these 'fields' declaration, result is the same
        # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        fields = UserCreationForm.Meta.fields 
        # + ('first_name', 'last_name', 'email',)

        widgets = {
            'username': forms.TextInput(attrs={'class': 'class="u-border-2 u-border-grey-5 u-grey-5 u-input u-input-rectangle u-radius-10"', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': "u-border-2 u-border-grey-5 u-grey-5 u-input u-input-rectangle u-radius-10", 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': "u-border-2 u-border-grey-5 u-grey-5 u-input u-input-rectangle u-radius-10", 'placeholder': 'Password Again'}),
            
            # 'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            # 'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            # 'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            
        }
        
        
        
        
        
#profile update

class UpdateForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ["username","email","first_name","last_name"]
        
