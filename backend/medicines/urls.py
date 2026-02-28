from django.urls import path
from .views import (
    DrugListView, DrugDetailView,
    ClinicStockListView, ClinicStockDetailView,
    StockAlertsView, NearbySurplusView
)

urlpatterns = [
    path('medicines/', DrugListView.as_view(), name='drug_list'),
    path('medicines/<int:pk>/', DrugDetailView.as_view(), name='drug_detail'),
    path('stock/', ClinicStockListView.as_view(), name='stock_list'),
    path('stock/<uuid:pk>/', ClinicStockDetailView.as_view(), name='stock_detail_update'),
    path('stock/alerts/', StockAlertsView.as_view(), name='stock_alerts'),
    path('stock/nearby-surplus/', NearbySurplusView.as_view(), name='stock_nearby_surplus'),
]
