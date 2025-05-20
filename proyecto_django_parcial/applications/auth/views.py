# applications/auth/views.py

from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        sex = request.POST.get('sex')
        country = request.POST.get('country')

        if password != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('auth:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
            return redirect('auth:register')

        hashed_password = make_password(password)
        User.objects.create(username=username, password=hashed_password, sex=sex, country=country)
        messages.success(request, 'Registro exitoso. Ahora inicia sesión.')
        return redirect('auth:login')

    return render(request, 'auth/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                messages.success(request, f'Bienvenido {user.username}')
                return redirect('games:games_list')
            else:
                messages.error(request, 'Contraseña incorrecta')
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')

    return render(request, 'auth/login.html')


def logout_view(request):
    request.session.flush()
    return redirect('games:games_list')
