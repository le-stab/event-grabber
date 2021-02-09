from django.http import request
from django.shortcuts import render
from .models import Event
from bs4 import BeautifulSoup
import requests

# Create your views here.


def event_day_view(request):
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
            speaker_name_beta = title.find('span')
            speaker_name = speaker_name_beta.getText().replace('with', '')
            title_name = title.getText().replace('with' + speaker_name, '')
            print('\ntalk name: %s | speaker name: %s' % (title_name, speaker_name))
        

        mp3 = requests.get(button['href'])
        msoup = BeautifulSoup(mp3.text, "html.parser")

        mp3s = msoup.find_all('source')

        for mp3_link in mp3s:
                #get mp3 link
                url = mp3_link['src']
                print(f'{url}')

                revised_name = f'{title_name} {speaker_name}'

                # remove invalid chars in mp3 link
                for char in invalid_chars:
                    revised_name = revised_name.replace(char, '')

                print(revised_name)

                

            # title = Event(title=speaker.getText())
            # title.save()

    return render(request, 'core/event.html')   
