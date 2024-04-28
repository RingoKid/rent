from django.db import models
from django.core.validators import MinValueValidator
from pydantic import BaseModel

class Tenant(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    identification_number = models.CharField(max_length=100)
    move_in_date = models.DateField()
    move_out_date = models.DateField(null=True, blank=True)  # Allow null and blank for move_out_date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    lease = models.ForeignKey('Lease', on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    month = models.IntegerField()
    year = models.IntegerField()
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction #{self.id}"


class Apartment(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)
    apartment_number = models.CharField(max_length=10)
    floor_number = models.IntegerField(validators=[MinValueValidator(1)])
    square_footage = models.IntegerField(validators=[MinValueValidator(1)])
    no_of_bedrooms = models.IntegerField()
    no_of_bathrooms = models.IntegerField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pet_policy = models.CharField(max_length=100)
    parking_fee = models.DecimalField(max_digits=10, decimal_places=2)
    apartment_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Apartment #{self.id}"


class Lease(models.Model):
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)
    apartment = models.ForeignKey('Apartment', on_delete=models.CASCADE)
    lease_start_date = models.DateField()
    lease_end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    lease_term = models.IntegerField()
    renewal_options = models.BooleanField(default=True)
    lease_document = models.FileField(upload_to='leases/', null=True, blank=True)
    LEASE_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Expired', 'Expired'),
        ('Terminated', 'Terminated'),
    ]
    lease_status = models.CharField(max_length=20, choices=LEASE_STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lease #{self.id}"

class MonthlyReportRequest(BaseModel):
    month: int
    year: int
    page_size: int
    page_number: int
    first_name: str = None
    last_name: str = None
    apartment_number: str = None
