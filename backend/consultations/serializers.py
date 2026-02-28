from rest_framework import serializers
from .models import Consultation, Message
from users.serializers import PatientSerializer, DoctorSerializer

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ConsultationSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Consultation
        fields = '__all__'
        read_only_fields = ['patient', 'id', 'created_at', 'started_at', 'ended_at', 'queue_position', 'status']

    def create(self, validated_data):
        patient = self.context['request'].user.patient_profile
        doctor_id = validated_data.pop('doctor_id', None)
        consultation = Consultation.objects.create(patient=patient, doctor_id=doctor_id, **validated_data)
        return consultation
