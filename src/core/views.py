from django.http import request
from django.shortcuts import render
from .models import Event, Speaker, TalkSession, EventTpl
from bs4 import BeautifulSoup
import requests
from .forms import EventSingleForm


# Create your views here.

def home_view(request):

    list = []
    form = EventSingleForm()

    if request.method == 'POST':
        filled_form = EventSingleForm(request.POST)
        if filled_form.is_valid():

            # TO DO: Check if URL can be opened AND CSS elements exits,
            #        IF NOT inform the user with an error

            # Get existing Event object from DB (Event Model) based on the "event_url" param and save it in POST_event_url var
            POST_event_url = filled_form.cleaned_data['event_url']
            selected_event = Event.objects.get(
                name=filled_form.cleaned_data['event_tpl'])

            # Get the Event Template Object  to access the CSS variables
            event_template = EventTpl.objects.get(
                name=selected_event.event_tpl)

            # Set CSS selectors from the existing Event Template object to use in BS4 objects
            css_link_button = event_template.css_link_button
            css_title = event_template.css_talk_title
            css_speaker_name = event_template.css_speaker_name
            css_photo = event_template.css_image
            css_audio_file = event_template.css_audio_file

            # Create a BS4 object for the INDEX_PAGE based on the url we got from POST_event_url
            # In our INDEX_page extract all the links using the CSS selector using css_link_button (Admin / Event)
            bs4_INDEX_PAGE_url = requests.get(POST_event_url)
            bs4_INDEX_PAGE_soup = BeautifulSoup(
                bs4_INDEX_PAGE_url.text, "html.parser")
            bs4_link_buttons = bs4_INDEX_PAGE_soup.select(css_link_button)
            bs4_photo = bs4_INDEX_PAGE_soup.select(css_photo)

            # print(bs4_photo['src'])
            # From the list of links iterate and create a new BS4 object so we can access each DETAIL_PAGE
            # Let's extract TITLE, SPEAKER_NAME and MP3_URL from this page
            for i, link in enumerate(bs4_link_buttons, start=0):
                try:   
                    bs4_DETAIL_PAGE_url = requests.get(link['href'])
                except:
                    continue
            
                bs4_DETAIL_PAGE_soup = BeautifulSoup(
                    bs4_DETAIL_PAGE_url.text, "html.parser")

                # Create SPEAKER_PHOTO list just containing the SRC value
                SPEAKER_PHOTO = bs4_photo[i]['src']

                # Get the TITLE using its CSS selector (from admin / Event), split() the string using 'with'
                # and return the first instance of the list created by the split() method
                # ie: "DIY Brain Health for Lifewith Peter Kan, DC, DACNB, FAAIM"
                # TO DO: We need to get the ELEMENT and the clean it in a different process, not the same line, based the website html structure
                TITLE = bs4_DETAIL_PAGE_soup.select_one(
                    css_title).text.split('with')[0]

                # Get the SPEAKER_NAME in SPAN using its CSS selector (from admin / Event), split() the string using ','
                # and return the first instance of the list created by the split() method, then use replace() and strip() white spaces
                # ie: "Peter Kan, DC, DACNB, FAAIM"
                # TO DO: We need to get the ELEMENT and the clean it in a different process, not the same line, based the website html structure
                SPEAKER_NAME = bs4_DETAIL_PAGE_soup.select_one(
                    css_speaker_name).text.split(',')[0].replace('with', '').strip()

                # Get MP3_URL
                MP3_URL = bs4_DETAIL_PAGE_soup.find(
                    css_audio_file)['src']

                # SPEAKER exists?
                # yes - just get existing id
                # no - create speaker and get id

                # Session exists?
                # yes - do nothing
                # no - create session and assign TITLE, SPEAKER_id, MP3_URL, EVENT
                # ADD creation date to handle future scenarios with the same session name but different dates

                # IF SPEAKER_NAME exists in DB (Speaker Model) get the ID
                if len(Speaker.objects.filter(name=SPEAKER_NAME)) != 0:
                    # Exists, get Speaker object
                    speaker_object = Speaker.objects.get(
                        name=SPEAKER_NAME)
                    print(f'SPEAKER exists: id {speaker_object.id}')
                else:
                    speaker_object = Speaker(
                        name=SPEAKER_NAME, img_url=SPEAKER_PHOTO)
                    speaker_object.get_remote_image()
                    print(f'SPEAKER [DOES NOT exists]: new speaker id {speaker_object.id}')
                    speaker_object.save()

                # Check if TalkSession already exists in DB
                if len(TalkSession.objects.filter(name=TITLE)) != 0:
                    # Exists, do nothing
                    print('TALK [exists]: Do nothing')
                    pass
                else:
                    new_talk_session = TalkSession(
                        name=TITLE, speaker=speaker_object, event=selected_event, mp3_url=MP3_URL)
                    new_talk_session.get_remote_mp3()
                    print(f'TALK [DOES NOT exists]: New talk id:{new_talk_session.id}, with speaker id: {speaker_object.name}, and event id: {selected_event.id}')
                    new_talk_session.save()

                list.append(
                    [[TITLE], [SPEAKER_NAME], [speaker_object.id], [MP3_URL], [bs4_photo[i]['src']]])

            return render(request, 'core/home.html', {'form': form, 'list': list})
    else:
        latest_talks = TalkSession.objects.all().order_by('-id')[:5]
        return render(request, 'core/home.html',
                      {'form': form,
                       'latest_talks': latest_talks
                       })


# List all TALK SESSIONS
def talks_list_view(request):
    # Get all sessions (order by date)
    list_talks = TalkSession.objects.all().order_by('-id')
    return render(request, 'core/talks_list.html', {'list_talks': list_talks})

# List all SPEAKERS


def speakers_list_view(request):
    speakers_list = Speaker.objects.all()
    return render(request, 'core/speaker_list_all.html', {'speakers_list': speakers_list})


def mock_view(request):
    test = Speaker.objects.all()
    return render(request, 'core/mock.html', {'test': test})
