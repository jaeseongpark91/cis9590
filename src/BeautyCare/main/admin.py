from django.contrib import admin
from .models import Clients, Salons, Services, Appointments

admin.site.register(Clients)
admin.site.register(Salons)
admin.site.register(Services)
admin.site.register(Appointments)