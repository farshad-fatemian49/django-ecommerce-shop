from http.client import HTTPResponse
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django import forms
from django.contrib import messages
from .forms import UpdateForm
from django.contrib.auth.models import User

# Create your views here.

# class RegisterView(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/register.html"
    
    
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display blank registration form. 
        form = UserCreationForm()
        form.fields['username'].widget = forms.TextInput(attrs={'class': "u-border-2 u-border-grey-5 u-grey-5 u-input u-input-rectangle u-radius-10",'placeholder': 'Your Username'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class': "u-border-2 u-border-grey-5 u-grey-5 u-input u-input-rectangle u-radius-10", 'placeholder': 'Password'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class': "u-border-2 u-border-grey-5 u-grey-5 u-input u-input-rectangle u-radius-10", 'placeholder': 'Password Again'})
        
        
        
    else:
        # Process completed form.
        form = UserCreationForm(data=request.POST)
 
        if form.is_valid():
            new_user = form.save()
        # Log in, redirect to home page.
            login(request, new_user)
            messages.success(request, 'Form submission successful')
            return redirect(request.path_info)
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request,'registration/register_final.html', context)



# from django.contrib.auth import login, authenticate
# from django.contrib.auth.views import LoginView
# from django.shortcuts import render, redirect

# from .forms import SignUpForm


# def register(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('product:product_list')
#     else:
#         form = SignUpForm()
#     context = {'form': form}
#     return render(request,'registration/register_final.html', context)


#change pass

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })
    
    
    
    
    #profile update
    
def update(request):
    if request.method == "POST":
        form = UpdateForm(data=request.POST , instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"profile Updated")
    else :
        form = UpdateForm(instance=request.user)
    return render(request,"registration/update_profile.html",{"form":form})



def DeleteAccount(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        user.delete()
        return HTTPResponse("your account deleted successfully")
    
    return render(request,"registration/DeleteAccount.html")
            