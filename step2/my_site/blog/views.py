from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from .models import Post
from users.forms import UserRegisterForm
from django.contrib.auth.models import User
from users.models import VerificationRequest
from users.forms import VerificationForm
from users import templates
from users.models import Profile
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)  # Получаем профиль пользователя
    return render(request, 'blog/user_detail.html', {'user': user})

def med_list(request):
    users = User.objects.all()
    return render(request, 'blog/med.html', {'users': users})

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


def about(request):
    if request.user.has_perm('your_app.admin_permission'):
        return render(request, 'blog/about.html', {'title': 'О клубе Python Bytes'})
    else: return render(request, 'blog/home.html')

def my_health(request):
    return render(request, 'blog/my_health.html')

def my_appointments(request):
    return render(request, 'blog/my_appointments.html')

def make_appointment(request):
    return render(request, 'blog/make_appointment.html')


def verify(request):

    
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            verification_code = form.cleaned_data['verification_code']
            try:
                verification_request = VerificationRequest.objects.get(
                    user=request.user,
                    verification_code=verification_code,
                    is_verified=False
                )
                verification_request.is_verified = True
                verification_request.save()
                return redirect('verification_success')
            except VerificationRequest.DoesNotExist:
                pass
    else:
        form = VerificationForm()

    return render(request, 'blog/verify.html', {'form': form})
