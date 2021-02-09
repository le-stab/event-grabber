from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ManyToManyField
from django.db.models.query import FlatValuesListIterable

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=60, blank=False)

    def __str__(self) -> str:
        return self.name


class Speaker(models.Model):
    name = models.CharField(max_length=30, blank=False)

    def __str__(self) -> str:
        return self.name


class TalkSession(models.Model):
    name = models.CharField(max_length=60, blank=False)
    speaker = models.ForeignKey(Speaker, on_delete=CASCADE)

    def __str__(self) -> str:
        return f"Event: {self.title}"


class Event(models.Model):
    name = models.CharField(
        blank=False, max_length=60, verbose_name='Event name')
    start_date = models.DateField(
        blank=True)
    duration = models.IntegerField(
        blank=True, default=1)
    category = models.ManyToManyField(Category)
    schedule = models.CharField(
        blank=True, max_length=20, verbose_name='Schedule path')
    landing_page = models.CharField(
        blank=False, max_length=100)
    css_link_button = models.CharField(
        max_length=20, blank=True, verbose_name='Button link (CSS)')
    css_image = models.CharField(
        max_length=20, blank=True, verbose_name='Photo (CSS)')
    css_talk_session = models.CharField(
        max_length=20, blank=True, verbose_name='Talk title (CSS)')
    css_audio_file = models.CharField(
        max_length=20, blank=True, verbose_name='Audio file (CSS)')
    css_video_file = models.CharField(
        max_length=20, blank=True, verbose_name='Video file (CSS)')
    scrape_ready = models.BooleanField(
        blank=True, default=False)

    def __str__(self) -> str:
        return f"{self.name}"
