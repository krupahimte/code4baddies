import uuid
from django.db import models
from users.models import Patient, Doctor, User

class Consultation(models.Model):
    TYPE_CHOICES = (
        ('ai_chat', 'AI Chat'),
        ('video', 'Video'),
        ('in_person', 'In Person'),
        ('async_chat', 'Async Chat'),
    )
    STATUS_CHOICES = (
        ('queued', 'Queued'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    TRIAGE_CHOICES = (
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('red', 'Red'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultations')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued')
    queue_position = models.IntegerField(null=True, blank=True)
    triage_level = models.CharField(max_length=10, choices=TRIAGE_CHOICES, null=True, blank=True)
    ai_summary = models.TextField(null=True, blank=True)
    agora_channel = models.CharField(max_length=100, null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'health_consultation'

class Message(models.Model):
    SENDER_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('ai', 'AI'),
    )
    INPUT_CHOICES = (
        ('text', 'Text'),
        ('voice', 'Voice'),
        ('image', 'Image'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='messages')
    sender_type = models.CharField(max_length=10, choices=SENDER_CHOICES)
    sender_id = models.UUIDField(null=True, blank=True) # UUID of patient or doctor
    content = models.TextField()
    content_en = models.TextField(null=True, blank=True)
    input_type = models.CharField(max_length=10, choices=INPUT_CHOICES, default='text')
    is_triage_result = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'health_message'
