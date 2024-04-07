from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

def home(request):
    if request.user.is_authenticated:
        button_text = 'IHALARIMIZ'
        button_url = reverse('all-uavs')
    else:
        button_text = 'GİRİŞ YAP'
        button_url = reverse('accounts:login')

    context = {
        'button_text': button_text,
        'button_url': button_url
    }
    return render(request, 'home.html', context)