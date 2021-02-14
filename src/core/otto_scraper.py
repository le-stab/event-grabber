from bs4 import BeautifulSoup
import requests
import json

from requests.api import get, head

'''
POST_event_url = 'https://theautoimmuneanswers.com/replays/?utm_source=ActiveCampaign&utm_medium=email&utm_content=%5BAutoimmune+Answers%5D+Replay+Marathon%3A+Binge+watch+your+favorite+episodes&utm_campaign=AIA+-+REPLAY+SATURDAY+e2+-+AFTERNOON+EMAIL&utm_source=ActiveCampaign&utm_medium=email&utm_content=%5BAutoimmune+Answers%5D+Save+up+to+93++during+our+Replay+Weekend&utm_campaign=AIA+-+REPLAY+SATURDAY+e3+-+EVENING+EMAIL'
css_link_button = '.pp-info-box-container'


bs4_INDEX_PAGE_url = requests.get(POST_event_url)
bs4_INDEX_PAGE_soup = BeautifulSoup(
    bs4_INDEX_PAGE_url.text, "html.parser")
bs4_link_buttons = bs4_INDEX_PAGE_soup.select(css_link_button)

for i, link in enumerate(bs4_link_buttons):
    bs4_DETAIL_PAGE_url = requests.get(link['href'])
    bs4_DETAIL_PAGE_soup = BeautifulSoup(
        bs4_DETAIL_PAGE_url.text, "html.parser")

    videos = bs4_DETAIL_PAGE_soup.select(
        '.elementor-video-iframe')
    print(f'Page :{i}')
    for video in videos:

        print(video['src'].replace('embed/', 'watch?v='))
        json.load()

'''


def get_yt_info(id):
    api_key = 'AIzaSyBpjQWfy0FVMet4n2FLqo8X-uhUvKk-8HQ'
    headers = {'user-agent': 'Mozilla/5.0'}
    url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={id}&key={api_key}'
    r = requests.get(url).json()
    for i in r['items']:
        for j in i['snippet']:
            print(j.title)

get_yt_info( 'u7XzHkUNIao')