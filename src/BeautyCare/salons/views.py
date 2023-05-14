from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import SalonCreationForm, ServiceCreationForm, SigninForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = SalonCreationForm(request.POST)
        if form.is_valid():
            result = form.save()
            if not result.get('success'):
                messages.warning(request, result.get('message'))
                return render(request, 'salons/registration.html', {'form': form})
            email = form.cleaned_data.get('email')
            request.session['email'] = email
            request.session['is_authenticated'] = True
            return redirect('salons-selectservices')
    if request.session.get('is_authenticated'):
        return redirect('salons-selectservices')
    form = SalonCreationForm()
    return render(request, 'salons/registration.html', {'form': form})

def select_services(request):
    if request.session.get('is_authenticated'):
        form = ServiceCreationForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                result = form.save(email=request.session.get('email'))
                return render(request, 'salons/services.html', context={'services': result.get('services', []), 'form': form})
        else:
            return render(request, 'salons/services.html', context={'services': form.get_services(request.session['email']), 'form': form})
    form = ServiceCreationForm()
    return render(request, 'salons/services.html', {'form': form})

def logout(request):
    del request.session['is_authenticated']
    del request.session['email']
    return redirect('main-home')

def signin(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            result = form.login()
            if not result.get('success'):
                messages.warning(request, result.get('message'))
                return render(request, 'salons/signin.html', {'form': form})
            request.session['email'] = form.data.get('email')
            request.session['is_authenticated'] = True
            return redirect('salons-selectservices')
    form = SigninForm()
    return render(request, 'salons/signin.html', {'form': form})