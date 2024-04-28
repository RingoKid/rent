from django.contrib import admin
from .models import Tenant, Transaction, Apartment, Lease

# Register your models here.
admin.site.register(Tenant)
admin.site.register(Transaction)
admin.site.register(Apartment)
admin.site.register(Lease)
