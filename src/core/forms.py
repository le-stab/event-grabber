from django import forms
from django.forms import Select, TextInput
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
