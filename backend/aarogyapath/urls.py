from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({"message": "Welcome to AarogyaPath API v1", "status": "online"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api_root),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('consultations.urls')),
    path('api/v1/', include('medicines.urls')),
]
