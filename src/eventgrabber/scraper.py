# https://mentalwellness.byhealthmeans.com/encore-weekend/?utm_source=ActiveCampaign&utm_medium=email&utm_content=Last+day+for+Encore+Weekend&utm_campaign=MNWL20

from bs4 import BeautifulSoup
import requests

insite = input('\n\nsite: ')


class Site:
    def __init__(self, site):
        self.site = site

    def ini(self):
        startpage = requests.get(self.site)
        bsoup = BeautifulSoup(startpage.text, "html.parser")
        buttons = bsoup.find_all('a', class_='button')

        for button in buttons:
            name = requests.get(button['href'])
            nsoup = BeautifulSoup(name.text, "html.parser")

            names = nsoup.find_all('h1', class_='presenter-title')

            for speaker in names:
                print(speaker.getText())


site = Site(insite)

site.ini()
