from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Subscriber

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_subcriber = Subscriber()
        new_subcriber.email = email
        new_subcriber.save()
        messages.info(request, "Successfully subscribed")
    return redirect('index')