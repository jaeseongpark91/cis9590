from address.models import AddressField
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class ClientsManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, password=None):
        if not email:
            raise ValueError('Email address is required')
        if not first_name:
            raise ValueError('First name is required')
        if not last_name:
            raise ValueError('Last name is required')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class SalonManager(BaseUserManager):
    def create_user(self, email, name, address, phone, password, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        if not name:
            raise ValueError('Business name is required')
        if not address:
            raise ValueError('Business address is required')
        if not phone:
            raise ValueError('Business phone number is required')
        if not password:
            raise ValueError('Password is required')

        salon = self.model(
            email=self.normalize_email(email),
            name=name,
            address=address,
            phone=phone,
            **extra_fields
        )

        salon.set_password(password)
        salon.save(using=self._db)
        return salon
    

class Clients(AbstractBaseUser):
    client_id = models.IntegerField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = PhoneNumberField(blank=True)

    objects = ClientsManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class Salons(models.Model):
    salon_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, unique=True)
    address = AddressField()
    phone = PhoneNumberField()
    website = models.URLField(max_length = 200, blank=True)
    password = models.CharField(max_length=100)
    

class Stylists(models.Model):
    stylist_id = models.IntegerField(primary_key=True)
    stylist_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    phone = PhoneNumberField(blank=True)
    salon_id = models.ForeignKey(Salons, on_delete=models.CASCADE)

class Reviews(models.Model):
    review_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=30)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    review_date = models.DateTimeField()
    salon_id = models.ForeignKey(Salons, on_delete=models.CASCADE)

class Services(models.Model):
    service_id = models.IntegerField(primary_key=True)
    service_name = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    salon_id = models.ForeignKey(Salons, on_delete=models.CASCADE)

class Appointments(models.Model):
    appointment_id = models.IntegerField(primary_key=True)
    appointment_date = models.DateTimeField()
    duration = models.IntegerField()
    notes = models.TextField(blank=True)
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Services, on_delete=models.CASCADE)

class Payments(models.Model):
    payment_id = models.IntegerField(primary_key=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_datetime = models.DateTimeField()
    appointment_id = models.ForeignKey(Appointments, on_delete=models.CASCADE)