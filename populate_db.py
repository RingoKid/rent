from quickstart.models import Tenant, Apartment
from faker import Faker

def add_tenants():
    # Create a Faker instance
    fake = Faker()

    # Create 10 new tenants
    for i in range(1, 11):
        tenant = Tenant(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone=fake.phone_number(),
            email=fake.email(),
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=90),
            identification_number=fake.unique.random_number(digits=9),
            move_in_date=fake.date_this_decade(before_today=True, after_today=False),
            move_out_date=None
        )
        tenant.save()

def add_apartments():
    # Create a Faker instance
    fake = Faker()

    # Create a list of apartment numbers
    apartment_numbers = [f"{i}{chr(j)}" for i in range(1, 11) for j in range(65, 91)]  # 65 to 91 are ASCII values for A to Z

    # Create new apartments
    for i in range(10):
        apartment = Apartment(
            address=fake.address(),
            apartment_number=apartment_numbers[i],
            floor_number=fake.random_int(min=1, max=10),
            square_footage=fake.random_int(min=500, max=2000),
            no_of_bedrooms=fake.random_int(min=1, max=4),
            no_of_bathrooms=fake.random_int(min=1, max=3),
            rent_amount=fake.random_int(min=1000, max=5000),
            security_deposit_amount=fake.random_int(min=500, max=1000),
            pet_policy=fake.random_element(elements=("Allowed", "Not Allowed")),
            parking_fee=fake.random_int(min=50, max=200),
            apartment_status=fake.random_element(elements=(True, False)),
        )
        apartment.save()