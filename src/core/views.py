from django.http import request
from django.shortcuts import render
from .models import Event

# Create your views here.


def event_view(request):
    return render(request, 'core/event.html')
