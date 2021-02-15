from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields.related import ManyToManyField
from django.core.files import File
import os
import urllib.request
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=60, blank=False)

    def __str__(self) -> str:
        return self.name


class Speaker(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    img_url = models.URLField(null=True, blank=True,
                              verbose_name='photo remote url')
    img_file = models.ImageField(
        upload_to="images", null=True, blank=True, verbose_name='photo file')
    website = models.CharField(max_length=100, blank=True, null=True)

    def get_remote_image(self):
        if self.img_url and not self.img_file:
            r = urllib.request.build_opener()
            r.addheaders = [("User-agent", "Mozilla/5.0")]
            urllib.request.install_opener(r)
            if os.path.isfile(os.path.basename(self.img_url)):
                print('-- ING Exists, do not save...')
                pass
            else:    
                result = urllib.request.urlretrieve(self.img_url, "")
                print('-- IMG does NOT exists, saving...')  
                self.img_file.save(
                    os.path.basename(self.img_url),
                    File(open(result[0], "rb")),
                )
                print('Done')
                self.save()


    def __str__(self) -> str:
        return self.name


class EventTpl(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    schedule_path = models.CharField(
        blank=True, null=True, max_length=20, verbose_name='Schedule path')
    css_link_button = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Button (CSS)')
    css_image = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Photo (CSS)')
    css_talk_title = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Title (CSS)')
    css_talk_topics = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='List of topics (CSS)')
    css_speaker_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Speaker name (CSS)')
    css_audio_file = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Audio file (CSS)')
    css_video_file = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Video file (CSS)')

    def __str__(self) -> str:
        return f'{self.name}'


class Event(models.Model):
    name = models.CharField(blank=False, max_length=60,
                            verbose_name='Event name')
    start_date = models.DateField(blank=True)
    duration = models.IntegerField(blank=True, default=1)
    category = models.ManyToManyField(Category)
    landing_page = models.CharField(blank=False, max_length=100)
    event_tpl = models.ForeignKey(
        EventTpl, on_delete=SET_NULL, blank=True, null=True)
    scrape_ready = models.BooleanField(blank=True, default=False)

    def __str__(self) -> str:
        return f'{self.name}'


class TalkSession(models.Model):
    name = models.CharField(max_length=60, null=True, blank=True,
                            verbose_name='Session name')
    speaker = models.ForeignKey(
        Speaker, on_delete=SET_NULL, verbose_name='Speaker name', null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=SET_NULL, null=True, blank=True)
    mp3_url = models.URLField(null=True, blank=True,
                              verbose_name='mp3 remote url')
    mp3_file = models.FileField(
        upload_to="mp3s", null=True, blank=True, verbose_name='mp3 file')

    def __str__(self) -> str:
        return f'Talk: {self.name}'

    def get_remote_mp3(self):
        if self.mp3_url and not self.mp3_file:
            r = urllib.request.build_opener()
            r.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(r)            
            if os.path.isfile(os.path.basename(self.mp3_url)):
                print('-- MP3 Exists, do not save...')
                pass
            else:
                print('-- MP3 does NOT exists, saving...')                
                result = urllib.request.urlretrieve(self.mp3_url, '')
                self.mp3_file.save(
                    f'{self.speaker} - {self.name}.mp3',
                    File(open(result[0], 'rb')),
                )
                print('Done')
                self.save()
