from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.query import FlatValuesListIterable

# Create your models here.


class Speaker(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name


class TalkSession(models.Model):
    name = models.CharField(max_length=60, blank=False)
    speaker = models.ForeignKey(Speaker, on_delete=CASCADE)

    def __str__(self) -> str:
        return f"Event: {self.title}"


class Event(models.Model):
    name = models.CharField(max_length=60, blank=False)
    start_date = models.DateField(blank=False)
    duration = models.DurationField(blank=False)
    landing_page = models.URLField()
    scrape_ready = models.BooleanField(default=False, blank=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.start_date}"
