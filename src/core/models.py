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
    name = models.CharField(max_length=60, blank=False)
    start_date = models.DateField(blank=True)
    duration = models.IntegerField(blank=True, default=1)
    category = models.ManyToManyField(Category)
    css_link_button = models.URLField()
    css_audio_file = models.URLField()
    scrape_ready = models.BooleanField(default=False, blank=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.start_date}"
