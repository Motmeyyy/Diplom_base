"""my_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from blog import views

from users.views import HeartRateView
from users.views import get_csrf_token
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('med/', views.med_list, name='user-list'),
    path('profile/edit/', user_views.edit_profile, name='edit_profile'),
    path('', include('blog.urls')),
    path('my_health/', views.my_health, name='my-health'),
    path('my_appointments/', user_views.view_appointments, name='view_appointments'),
    path('make_appointment/', user_views.create_appointment, name='create_appointment'),
    path('doctor_appointments/', user_views.doctor_appointments, name='doctor_appointments'),
    path('purchase-history/', user_views.purchase_history, name='purchase_history'),
    path('users/', user_views.user_list, name='user_list'),
    path('message/send/<int:recipient_id>/', user_views.message_send, name='message_send'),

    path('message/view/<int:recipient_id>/', user_views.message_view, name='message_view'),
    path('message/view/patient/', user_views.message_view_patient, name='message_view_patient'),
    path('message/view/doctor/', user_views.message_view_doctor, name='message_view_doctor'),
    path('chat/delete/patient/<int:doctor_id>/', user_views.chat_delete_patient, name='chat_delete_patient'),

    path('api/heart_rate/', HeartRateView.as_view(), name='heart_rate_api'),
    path('chat/delete/<int:recipient_id>/', user_views.chat_delete, name='chat_delete'),
    path('api/get_heart_rate/', HeartRateView.as_view(), name='get_heart_rate'),
    path('api/get_csrf_token/', user_views.get_csrf_token, name='get_csrf_token'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)