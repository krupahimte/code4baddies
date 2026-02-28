from rest_framework import generics, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Drug, ClinicStock
from .serializers import DrugSerializer, ClinicStockSerializer

class DrugListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name_en', 'brand_names', 'uses_en']

class DrugDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer

class ClinicStockListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClinicStockSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctor_profile') and user.doctor_profile.clinic:
            qs = ClinicStock.objects.filter(clinic=user.doctor_profile.clinic)
            alert = self.request.query_params.get('alert')
            if alert == 'true':
                # Simplified alert logic
                pass # Need proper filter based on min threshold
            return qs
        return ClinicStock.objects.none()

class ClinicStockDetailView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClinicStockSerializer
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctor_profile') and user.doctor_profile.clinic:
            return ClinicStock.objects.filter(clinic=user.doctor_profile.clinic)
        return ClinicStock.objects.none()

class StockAlertsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response({
            "success": True,
            "data": []
        })

class NearbySurplusView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response({
            "success": True,
            "data": []
        })
