from address.forms import AddressField, Address
from django import forms
from django.contrib.auth.hashers import make_password, check_password
from main.models import Salons, Services
from phonenumber_field.formfields import PhoneNumberField

class SalonCreationForm(forms.Form):
    name = forms.CharField(label='Business Name', max_length=80)
    email = forms.EmailField()
    phone = PhoneNumberField(label='Business Phone Number')
    address = AddressField(label='Business Address')
    website = forms.CharField(label='Business Website URL (if applicable)', required=False)
    password = forms.CharField(min_length=8, max_length=32, widget=forms.PasswordInput)
    passwordc = forms.CharField(min_length=8, max_length=32, widget=forms.PasswordInput, label='Confirm Password')
    # class Meta:
    #     model = Salons
    #     fields = ('name', 'address', 'phone', 'website', 'password', 'passwordc')
    
    def save(self):
        if Salons.objects.filter(email=self.data['email']):
            return {'success': False, 'message': 'An account already exist for this email address.'}
        data = {field.name: self.data.get(field.name) for field in Salons._meta.get_fields() if field.name in self.data}
        data['password'] = make_password(data['password'])
        data['address'] = self._get_address_object(self.data)
        Salons.objects.create(**data)
        return {'success': True}
    
    def _get_address_object(self, data):
        # django-address became a bit tricky. Just creating the correct object manually
        google_to_django_object_mapping = {
            'address_country': 'country',
            'address_country_code': 'country_code',
            'address_locality': 'locality',
            'address_postal_code': 'postal_code',
            'address_route': 'route',
            'address_street_number': 'street_number',
            'address_state': 'state',
            'address_state_code': 'state_code',
            'address_formatted': 'raw',
            'address_latitude': 'latitude',
            'address_longitude': 'longitude'
            }
        address_obj = {}
        for field in data:
            if field in google_to_django_object_mapping:
                address_obj[google_to_django_object_mapping[field]] = data.get(field)
        if 'locality' in address_obj:
            address_obj['locality'] = {
                'name': address_obj.get('locality', ''),
                'postal_code': address_obj.get('postal_code', ''),
                'state':address_obj.get('state', '')
                }
        return address_obj


class ServiceCreationForm(forms.Form):
    service_name = forms.CharField(max_length=300, label="Service Name")
    description = forms.CharField(label="Service Description")
    price = forms.DecimalField(label="Price US$", max_digits=6, decimal_places=2)

    def save(self, email=None):
        salon = Salons.objects.filter(email=email).first()
        if salon:
            data = {field.name: self.data.get(field.name) for field in Services._meta.get_fields() if field.name in self.data}
            data['salon_id'] = salon
            Services.objects.create(**data)
            return {'success': True, 'services': self.get_services(email, salon_id=salon.salon_id)}
        return {'success': False, 'message': 'Could not find a valid account for salon.'}
    
    def get_services(self, email, salon_id=None):
        if salon_id:
            return list(Services.objects.filter(salon_id=salon_id).values('service_name', 'description', 'price'))
        salon = Salons.objects.filter(email=email).first()
        return list(Services.objects.filter(salon_id=salon.salon_id).values('service_name', 'description', 'price'))

class SigninForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=8, max_length=32, widget=forms.PasswordInput)

    def login(self):
        salon = Salons.objects.filter(email=self.data.get('email')).first()
        if salon:
            if check_password(self.data.get('password'), salon.password):
                return {'success': True}
            return {'success': False, 'message': 'Incorrect password. Try again.'}
        return {'success': False, 'message': 'An account does not exist with the provided email address.'}