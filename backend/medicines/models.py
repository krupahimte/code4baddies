import uuid
from django.db import models
from users.models import Clinic

class Drug(models.Model):
    name_en = models.CharField(max_length=200)
    brand_names = models.TextField(null=True, blank=True)
    drug_class = models.CharField(max_length=100, null=True, blank=True)
    uses_en = models.TextField()
    dosage_json = models.TextField(null=True, blank=True)
    side_effects_en = models.TextField(null=True, blank=True)
    warnings_en = models.TextField(null=True, blank=True)
    interactions = models.TextField(null=True, blank=True)
    schedule = models.CharField(max_length=5, null=True, blank=True)
    jan_aushadhi = models.BooleanField(default=False)
    price_min_paise = models.IntegerField(null=True, blank=True)
    price_max_paise = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'medicine_drug'

class ClinicStock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='stock')
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='clinics')
    current_qty = models.IntegerField()
    min_threshold = models.IntegerField()
    avg_daily_usage = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    predicted_stockout = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clinic_stock'
