from rest_framework import serializers
from .models import Tenant, Transaction, Apartment, Lease


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = '__all__'


class LeaseSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only=True)
    apartment = ApartmentSerializer(read_only=True)

    class Meta:
        model = Lease
        fields = '__all__'
