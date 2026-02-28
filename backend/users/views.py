from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Patient, Doctor
from .serializers import PatientSerializer, DoctorSerializer

class SendOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        phone = request.data.get('phone_number')
        if not phone:
            return Response({"error": {"message": "phone_number required"}}, status=status.HTTP_400_BAD_REQUEST)
        # Mock OTP send
        return Response({"success": True})

class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        phone = request.data.get('phone_number')
        otp = request.data.get('otp')
        
        if not phone or not otp:
            return Response({"error": {"message": "phone_number and otp required"}}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            user = User.objects.get(phone_number=phone)
            user.is_verified = True
            user.save()
            
            refresh = RefreshToken.for_user(user)
            
            # Identify profile
            profile_data = None
            if hasattr(user, 'patient_profile'):
                profile_data = PatientSerializer(user.patient_profile).data
            elif hasattr(user, 'doctor_profile'):
                profile_data = DoctorSerializer(user.doctor_profile).data
                
            return Response({
                "success": True,
                "data": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": profile_data
                }
            })
        except User.DoesNotExist:
            return Response({"error": {"code": "PATIENT_NOT_FOUND", "message": "User not found. Please register."}}, status=status.HTTP_404_NOT_FOUND)

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        phone = request.data.get('phone_number')
        name = request.data.get('name')
        if not phone or not name:
            return Response({"error": {"message": "phone_number and name required"}}, status=status.HTTP_400_BAD_REQUEST)
            
        user, created = User.objects.get_or_create(phone_number=phone, defaults={'name': name, 'is_verified': True, 'role': 'patient'})
        patient, _ = Patient.objects.get_or_create(user=user)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            "success": True,
            "data": {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": PatientSerializer(patient).data
            }
        })

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"success": True})
        except Exception:
            # For simplicity without blacklist app installed properly we just return success
            return Response({"success": True})

class PatientProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if not hasattr(user, 'patient_profile'):
            return Response({"error": {"message": "Not a patient"}}, status=status.HTTP_403_FORBIDDEN)
            
        profile = user.patient_profile
        return Response({
            "success": True,
            "data": {
                "patient": PatientSerializer(profile).data,
                "vitals": [],
                "upcoming": []
            }
        })

    def patch(self, request):
        user = request.user
        if not hasattr(user, 'patient_profile'):
            return Response({"error": {"message": "Not a patient"}}, status=status.HTTP_403_FORBIDDEN)
            
        profile = user.patient_profile
        # simple update logic
        if 'name' in request.data:
            user.name = request.data['name']
            user.save()
            
        # Update patient fields
        for field in ['language_pref', 'district', 'state']:
            if field in request.data:
                setattr(profile, field, request.data[field])
        profile.save()
        
        return Response({
            "success": True,
            "data": {
                "patient": PatientSerializer(profile).data
            }
        })

class DoctorListView(APIView):
    def get(self, request):
        doctors = Doctor.objects.filter(is_available=True)
        # handle ?lang=hi filtering if needed
        language = request.query_params.get('lang')
        if language:
            doctors = doctors.filter(languages__icontains=language)
            
        data = DoctorSerializer(doctors, many=True).data
        return Response({
            "success": True,
            "data": data,
            "meta": {
                "total": doctors.count()
            }
        })

class DoctorDetailView(APIView):
    def get(self, request, pk):
        try:
            doctor = Doctor.objects.get(user__id=pk)
            return Response({
                "success": True,
                "data": {
                    "doctor": DoctorSerializer(doctor).data,
                    "reviews": []
                }
            })
        except Doctor.DoesNotExist:
            return Response({"error": {"message": "Doctor not found"}}, status=status.HTTP_404_NOT_FOUND)
