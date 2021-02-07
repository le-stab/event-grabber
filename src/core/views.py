from django.http import request
from django.shortcuts import render
from .models import Event
from bs4 import BeautifulSoup
import requests

# Create your views here.


def event_view(request):
    url = 'https://mentalwellness.byhealthmeans.com/encore-weekend/?utm_source=ActiveCampaign&utm_medium=email&utm_content=Last+day+for+Encore+Weekend&utm_campaign=MNWL20'

    startpage = requests.get(url)
    bsoup = BeautifulSoup(startpage.text, "html.parser")
    buttons = bsoup.find_all('a', class_='button')

    for button in buttons:
        name = requests.get(button['href'])
        nsoup = BeautifulSoup(name.text, "html.parser")

        talktitle = nsoup.find_all('h1', class_='presenter-title')

        for title in talktitle:
            speakernamebeta = title.find('span')
            speakername = speakernamebeta.getText().replace('with', '')
            titlename = title.getText().replace('with' + speakername, '')
            print('talk name: %s | speaker name: %s' % (titlename, speakername))

            # title = Event(title=speaker.getText())
            # title.save()

    return render(request, 'core/event.html')   
