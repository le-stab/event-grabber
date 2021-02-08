from django.http import request
from django.shortcuts import render
from .models import Event
from bs4 import BeautifulSoup
import requests

# Create your views here.


def event_day_view(request):
    global titlename
    global speakername
    invalid_chars = ''':*"?|'''
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
        

        mp3 = requests.get(button['href'])
        msoup = BeautifulSoup(mp3.text, "html.parser")

        mp3s = msoup.find_all('source')

        for m in mp3s:
                #get mp3 link
                url = m['src']
                print(f'{url}')

                revisedstr = f'{titlename} {speakername}'

                # remove invalid chars in mp3 link
                for char in invalid_chars:
                    revisedstr = revisedstr.replace(char, '')

                print(revisedstr)

                

            # title = Event(title=speaker.getText())
            # title.save()

    return render(request, 'core/event.html')   
