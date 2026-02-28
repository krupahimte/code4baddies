from django.urls import path
from .views import (
    ConsultationListView, ConsultationDetailView,
    AgoraTokenView, QueuePositionView,
    AIChatView, AITriageView, AIChatHistoryView
)

urlpatterns = [
    path('consultations/', ConsultationListView.as_view(), name='consultation_list'),
    path('consultations/<uuid:pk>/', ConsultationDetailView.as_view(), name='consultation_detail'),
    path('consultations/<uuid:pk>/agora-token/', AgoraTokenView.as_view(), name='agora_token'),
    path('queue/position/', QueuePositionView.as_view(), name='queue_position'),
    path('ai/chat/', AIChatView.as_view(), name='ai_chat'),
    path('ai/triage/', AITriageView.as_view(), name='ai_triage'),
    path('ai/chat/history/<uuid:id>/', AIChatHistoryView.as_view(), name='ai_chat_history'),
]
