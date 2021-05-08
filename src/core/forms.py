from django import forms
from django.forms import Select, TextInput
from .models import Event


class EventSingleForm(forms.Form):
    # Create an empty input to pass the event DAY to scrape
    event_day = forms.CharField(
        label='Day: ',
        required=False,
        widget=TextInput(attrs={'class': 'form-control', 'size': '10'}),
    )
    # Create drop-down select based on all the objects in Event model
    event_tpl = forms.ModelChoiceField(
        label='Event: ',
        required=True,
        widget=Select(attrs={'class': 'form-select'}),
        queryset=Event.objects.all())
