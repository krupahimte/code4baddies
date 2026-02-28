import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .models import Consultation, Message
from .models import Consultation, Message
from .serializers import ConsultationSerializer, MessageSerializer
from agora_token_builder import RtcTokenBuilder
import uuid

Role_Publisher = 1

class ConsultationListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConsultationSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'patient_profile'):
            return Consultation.objects.filter(patient=user.patient_profile).order_by('-created_at')
        if hasattr(user, 'doctor_profile'):
            return Consultation.objects.filter(doctor=user.doctor_profile).order_by('-created_at')
        return Consultation.objects.none()

class ConsultationDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConsultationSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'patient_profile'):
            return Consultation.objects.filter(patient=user.patient_profile)
        if hasattr(user, 'doctor_profile'):
            return Consultation.objects.filter(doctor=user.doctor_profile)
        return Consultation.objects.none()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        messages = Message.objects.filter(consultation=instance).order_by('created_at')
        return Response({
            "success": True,
            "data": {
                "consultation": serializer.data,
                "messages": MessageSerializer(messages, many=True).data
            }
        })

class AgoraTokenView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            consultation = Consultation.objects.get(id=pk)
            # Permission check omitted for brevity
            
            app_id = os.environ.get("AGORA_APP_ID", "mock_id")
            app_cert = os.environ.get("AGORA_APP_CERT", "mock_cert")
            channel = str(pk)
            uid = 1 if hasattr(request.user, 'patient_profile') else 2
            
            token = RtcTokenBuilder.buildTokenWithUid(
                app_id, app_cert, channel, uid, Role_Publisher, 3600
            )
            
            return Response({
                "success": True,
                "data": {
                    "token": token,
                    "channel": channel,
                    "uid": uid,
                    "app_id": app_id
                }
            })
        except Consultation.DoesNotExist:
            return Response({"error": {"message": "Consultation not found"}}, status=status.HTTP_404_NOT_FOUND)

class QueuePositionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            "success": True,
            "data": {
                "position": 1,
                "eta_minutes": 10
            }
        })

class AIChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        text = request.data.get('text', '')
        # Mocking Gemini Response for now
        return Response({
            "success": True,
            "data": {
                "reply": "This is a mock response from Gemini AI. Please contact a doctor if symptoms persist.",
                "triage_level": "green",
                "msg_id": str(uuid.uuid4())
            }
        })

class AITriageView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        return Response({
            "success": True,
            "data": {
                "level": "yellow",
                "advice": "Hydrate and rest.",
                "recommend_doctor": True
            }
        })

class AIChatHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, id):
        messages = Message.objects.filter(consultation_id=id).order_by('created_at')
        return Response({
            "success": True,
            "data": MessageSerializer(messages, many=True).data
        })
