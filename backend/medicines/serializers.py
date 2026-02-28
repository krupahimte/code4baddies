from rest_framework import serializers
from .models import Drug, ClinicStock

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = '__all__'

class ClinicStockSerializer(serializers.ModelSerializer):
    drug = DrugSerializer(read_only=True)
    
    class Meta:
        model = ClinicStock
        fields = '__all__'
