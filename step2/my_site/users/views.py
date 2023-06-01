from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .forms import UserRegisterForm
from .forms import UserUpdateForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            
            user = form.save()
            group = form.cleaned_data['group']
            group.user_set.add(user)
            login(request, user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})




@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/profile.html', context)

