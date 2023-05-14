from django.urls import path
from . import views

urlpatterns = [
    path('registration', views.register, name='salons-register'),
    path('services', views.select_services, name='salons-selectservices'),
    path('logout', views.logout, name='salons-logout'),
    path('signin', views.signin, name='salons-signin')
]