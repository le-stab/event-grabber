from django.http import request
from django.shortcuts import render
from .models import Event
from bs4 import BeautifulSoup
import requests
from .forms import EventSingleForm

# Create your views here.


def event_single_view(request):

    list = []
    event_single_form = EventSingleForm

    if request.method == 'POST':
        filled_form = EventSingleForm(request.POST)
        if filled_form.is_valid():

            invalid_chars = ''':*"?|'''
            url = filled_form.cleaned_data['event_url']
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
                    print('\ntalk name: %s | speaker name: %s' %
                          (title_name, speaker_name))

                mp3 = requests.get(button['href'])
                msoup = BeautifulSoup(mp3.text, "html.parser")

                mp3s = msoup.find_all('source')

                for mp3_link in mp3s:
                    # get mp3 link
                    mp3_url = mp3_link['src']
                    print(f'{mp3_url}')

                    revised_name = f'{title_name} {speaker_name}'

                    # remove invalid chars in mp3 link
                    for char in invalid_chars:
                        revised_name = revised_name.replace(char, '')

                    print(revised_name)

                list.append(f'{revised_name} | {mp3_url} ')
            print(filled_form.cleaned_data['event_url'])
            return render(request, 'core/event_single.html', {'list': list})
    else:
        form = EventSingleForm()
        return render(request, 'core/event_single.html', {'form': form, 'list': list})
