from typing import Text
from django import forms
from django.db.models.query import QuerySet
from django.forms import fields, widgets
from django.forms import ModelForm, SelectMultiple, Select, TextInput
from django.db import models
from .models import Event


class EventSingleForm(forms.Form):
    # Create an empty input to pass the URL to scrape
    event_url = forms.CharField(
        label='Event URL: ',
        widget=TextInput(attrs={'class': 'form-control', 'size': '80'}),
    )
    # Create drop-down select based on all the objects in Event model
    event_tpl = forms.ModelChoiceField(
        label='Event: ',
        required=True,
        widget=Select(attrs={'class': 'form-select'}),
        queryset=Event.objects.all())
