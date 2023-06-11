from django.http import JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from . import views
from .views import verify
from users import views as user_views
from django.conf.urls.static import static
from django.conf import settings

from users.views import HeartRateView


@require_GET
@csrf_exempt
def csrf_token(request):
    from django.middleware.csrf import get_token
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('med/', views.med_list, name='med-list'),
    path('med/<int:user_id>/', views.user_detail, name='user-detail'),
    path('verify/', verify, name='verify'),
    path('my_health/', views.my_health, name='my-health'),

    path('my_appointments/', user_views.view_appointments, name='view_appointments'),
    path('make_appointment/', user_views.create_appointment, name='create_appointment'),
    path('med/search/', views.search_users, name='search-users'),

]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)