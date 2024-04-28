from django.urls import path
from .views import ApartmentViewSet, apartment_status_count, active_lease_rent_sum, current_month_year_transaction_sum, \
    rent_and_transaction_summary, tenant_info, tenant_detail, LeaseViewSet, monthly_report

from quickstart.views import TenantViewSet

urlpatterns = [
    path('tenants/', TenantViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('tenants/<int:pk>/', TenantViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('apartments/', ApartmentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('apartments/<int:pk>/', ApartmentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('apartment-status-count/', apartment_status_count),
    path('active-lease-rent-sum/', active_lease_rent_sum),
    path('current-month-year-transaction-sum/', current_month_year_transaction_sum),
    path('rent-and-transaction-summary/', rent_and_transaction_summary),
    path('tenant-info/', tenant_info),
    path('tenant-detail/<int:tenant_id>/', tenant_detail),
    path('lease/', LeaseViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('lease/<int:pk>/', LeaseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('monthly-report/', monthly_report, name='monthly-report'),
]