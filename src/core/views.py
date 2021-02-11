from django.http import request
from django.shortcuts import render
from .models import Event, Speaker, TalkSession
from bs4 import BeautifulSoup
import requests
from .forms import EventSingleForm


# Create your views here.

def event_single_view(request):

    list = []
    form = EventSingleForm()

    if request.method == 'POST':
        filled_form = EventSingleForm(request.POST)
        if filled_form.is_valid():

            # TO DO: Check if URL can be opened AND CSS elements exits,
            #        IF NOT inform the user with an error

            # Get existing Event object from DB (Event Model) based on the "event_url" param and save it in POST_event_url var
            POST_event_url = filled_form.cleaned_data['event_url']
            existing_event_tpl_object = Event.objects.get(
                name=filled_form.cleaned_data['event_tpl'])

            # Set CSS selectors from the existing Event object so these vars can be used in the different BS4 objects
            css_link_button = existing_event_tpl_object.css_link_button
            css_title = existing_event_tpl_object.css_talk_session
            css_speaker_name = existing_event_tpl_object.css_speaker_name
            css_audio_file = existing_event_tpl_object.css_audio_file

            # Create a BS4 object for the INDEX_PAGE based on the url we got from POST_event_url
            # In our INDEX_page extract all the links using the CSS selector using css_link_button (Admin / Event)
            bs4_INDEX_PAGE_url = requests.get(POST_event_url)
            bs4_INDEX_PAGE_soup = BeautifulSoup(
                bs4_INDEX_PAGE_url.text, "html.parser")
            bs4_link_buttons = bs4_INDEX_PAGE_soup.select(css_link_button)
            bs4_speaker_name = bs4_INDEX_PAGE_soup.select(css_link_button)

            # From the list of links iterate and create a new BS4 object so we can access each DETAIL_PAGE
            # Let's extract TITLE, SPEAKER_NAME and AUDIO_FILE from this page
            for link in bs4_link_buttons:
                bs4_DETAIL_PAGE_url = requests.get(link['href'])
                bs4_DETAIL_PAGE_soup = BeautifulSoup(
                    bs4_DETAIL_PAGE_url.text, "html.parser")

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

                # Get AUDIO_FILE
                AUDIO_FILE = bs4_DETAIL_PAGE_soup.find(
                    css_audio_file)['src']

                # SPEAKER exists?
                # yes - just get existing id
                # no - create speaker and get id

                # Session exists?
                # yes - do nothing
                # no - create session and assign TITLE, SPEAKER_id, AUDIO_FILE, EVENT
                # ADD creation date to handle future scenarios with the same session name but different dates

                # IF SPEAKER_NAME exists in DB (Speaker Model) get the ID
                if len(Speaker.objects.filter(name=SPEAKER_NAME)) != 0:
                    # Exists, get Speaker object
                    speaker_object = Speaker.objects.get(
                        name=SPEAKER_NAME)
                    print(f'speaker exists: id {speaker_object.id}')
                else:
                    speaker_object = Speaker(name=SPEAKER_NAME)
                    speaker_object.save()
                    print(
                        f'speaker does  NOT exists: new speaker id {speaker_object.id}')

                # Check if TalkSession already exists in DB
                if len(TalkSession.objects.filter(name=TITLE)) != 0:
                    # Exists, do nothing
                    print('talk session exists: do nothing')
                    pass
                else:
                    new_talk_session = TalkSession(
                        name=TITLE, speaker=speaker_object, event=existing_event_tpl_object, audio_file_path=AUDIO_FILE)
                    new_talk_session.save()
                    print(
                        f'talk session does NOT exists: new session id:{new_talk_session.id}, with speaker id: {speaker_object.id}, and event id: {existing_event_tpl_object.id}')

                list.append(
                    f"{TITLE} ||| {SPEAKER_NAME} ({speaker_object.id}) ||| {AUDIO_FILE}")

            return render(request, 'core/event_single.html', {'form': form, 'list': list})
    else:
        return render(request, 'core/event_single.html', {'form': form, })

# List all TALK SESSIONS


def talk_sessions_list_view(request):
    # Get all sessions (order by date)
    talk_sessions_list = TalkSession.objects.all()
    return render(request, 'core/talk_sessions_list.html', {'talk_sessions_list': talk_sessions_list})

# List all SPEAKERS


def speakers_list_view(request):
    speakers_list = Speaker.objects.all()
    return render(request, 'core/speaker_list_all.html', {'speakers_list': speakers_list})


def mock_view(request):
    test = Speaker.objects.all()
    return render(request, 'core/mock.html', {'test': test})


def home_view(request):
    return render(request, 'core/home.html')
