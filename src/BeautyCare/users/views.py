from django.shortcuts import render, redirect
from .forms import ClientCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        request.POST.get('timeInput')
        form = ClientCreationForm(request.POST)
        if form.is_valid():
            result = form.save(request)
            messages.success(request, result.get('message'))
            return redirect('main-home')
    request.session['appointment_time'] = request.GET.get('timeInput')
    form = ClientCreationForm()
    return render(request, 'users/register.html', {'form': form})
