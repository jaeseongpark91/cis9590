import datetime
from django import forms
from main.models import Clients, Appointments, Services
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField

class ClientCreationForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(label='First name', required=True)
    last_name = forms.CharField(label='Last name', required=True)
    phone = PhoneNumberField()

    def save(self, request):
        appointment_time = request.session['appointment_time']
        service_id = Services.objects.filter(service_id=request.session['service_id']).first()
        client = Clients.objects.filter(email=self.data.get('email')).first()
        if not client:
            data = {field.name: self.data.get(field.name) for field in Clients._meta.get_fields() if field.name in self.data}
            Clients.objects.create(**data)
            client = Clients.objects.filter(email=self.data.get('email')).first()

        appointment = {
            'client_id': client,
            'service_id': service_id,
            'appointment_date': datetime.datetime.strptime(appointment_time, '%Y-%m-%d %H:%M:%S'),
            'duration': 1,
            'notes': ''
        }
        Appointments.objects.create(**appointment)
        return {'success': True, 'message': 'Appointment scheduled!'}
