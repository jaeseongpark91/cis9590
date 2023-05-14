import datetime
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Salons, Services, Appointments
from address.models import Address
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

@ensure_csrf_cookie
def home(request):
    if request.method == 'POST':
        services = Services.objects.filter(salon_id=request.POST.get('salonID')).values('service_id', 'service_name', 'description', 'price')
        ctx = {'services': services, 'csrf_token': request.POST['csrfmiddlewaretoken']}
        return render(request, 'scheduling/service-selection.html', context=ctx)
    return render(request, 'home/home.html')

def select_time(request):
    if request.method == 'POST':
        service_id = request.POST.get('svcChkbx')
        request.session['service_id'] = service_id
        return render(request, 'scheduling/appointment-time.html')
    return redirect('main-home')

@csrf_exempt
def available_times(request):
    data = json.loads(request.body)
    date = datetime.datetime.strptime(data['date'], '%Y-%m-%d')
    times_available = []
    salon = Services.objects.filter(service_id=request.session['service_id']).first()
    services_available = Services.objects.filter(salon_id=salon.salon_id).values('service_id')
    existing_appointments = Appointments.objects.filter(appointment_date__date=date.date(), service_id__in=services_available).values()
    taken = {appointment['appointment_date'].hour for appointment in existing_appointments}

    if date.date() == datetime.datetime.now().date():
        for hour in range(0, datetime.datetime.today().hour + 1):
            taken.add(hour)
            
    while date.hour <= 20:
        if date.hour >= 9:
            times_available.append({'text': date.strftime('%H:%M'), 'time': str(date), 'available': False if date.hour in taken else True})
        date = date + datetime.timedelta(hours=1)
    return JsonResponse(times_available, safe=False)


def auto_complete(request):
    if request.GET.get('q'):
        q = request.GET['q']
        data = Salons.objects.filter(name__startswith=q).values('name', 'address', 'salon_id')
        json = []
        for item in data:
            out = {}
            adr = Address.objects.filter(pk=item.get('address')).first()
            out['text'] = item['name'] + ' - ' + adr.raw
            out['id'] = item.get('salon_id')
            json.append(out)
        return JsonResponse(json, safe=False)
    else:
        HttpResponse("No cookies")