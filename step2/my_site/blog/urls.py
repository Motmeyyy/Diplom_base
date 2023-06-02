from django.urls import path
from . import views
from .views import verify
from users import views as user_views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('med/', views.med_list, name='med-list'),
    path('med/<int:user_id>/', views.user_detail, name='user-detail'),
    path('verify/', verify, name='verify'),
    path('my_health/', views.my_health, name='my-health'),

    path('my_appointments/', user_views.view_appointments, name='view_appointments'),
    path('make_appointment/', user_views.create_appointment, name='create_appointment'),

]