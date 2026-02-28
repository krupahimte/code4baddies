from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    SendOTPView, VerifyOTPView, RegisterView, LogoutView,
    PatientProfileView, DoctorListView, DoctorDetailView
)

urlpatterns = [
    path('auth/otp/send/', SendOTPView.as_view(), name='otp_send'),
    path('auth/otp/verify/', VerifyOTPView.as_view(), name='otp_verify'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('patient/profile/', PatientProfileView.as_view(), name='patient_profile'),
    path('doctors/', DoctorListView.as_view(), name='doctor_list'),
    path('doctors/<uuid:pk>/', DoctorDetailView.as_view(), name='doctor_detail'),
]
