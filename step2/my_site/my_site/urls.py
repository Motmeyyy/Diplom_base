from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from blog import views
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
    path('diets/', user_views.diet_list, name='diet_list'),
    path('recipes/', user_views.recipe_list, name='recipe_list'),
    path('diets/<int:diet_id>/', user_views.diet_detail, name='diet_detail'),
    path('diets/<int:diet_id>/choose/', user_views.choose_diet, name='choose_diet'),
    path('diets_main/', user_views.diets_main, name='diets_main'),
    path('create_diet/', user_views.create_diet, name='create_diet'),
    path('create_recipe/', user_views.create_recipe, name='create_recipe'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)