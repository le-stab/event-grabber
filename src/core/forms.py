from django import forms


class EventSingleForm(forms.Form):
    event_url = forms.CharField(label='Event URL: ')
