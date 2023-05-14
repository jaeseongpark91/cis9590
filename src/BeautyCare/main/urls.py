from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('business-auto-complete', views.auto_complete, name='main-autocomplete'),
    path('select-time', views.select_time, name='main-select-time'),
    path('available-times', views.available_times, name='main-available-times')
]