from django.shortcuts import render, redirect
from django.contrib.auth import logout

def login_view(request):
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('core:core')

def register(request):
    return render(request, 'auth/register.html')