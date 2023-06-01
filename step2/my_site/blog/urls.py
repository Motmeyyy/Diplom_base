from django.urls import path
from . import views
from .views import verify
urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('med/', views.med_list, name='med-list'),
    path('med/<int:user_id>/', views.user_detail, name='user-detail'),
    path('verify/', verify, name='verify'),
]