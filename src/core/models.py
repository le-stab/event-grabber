from django.db import models

# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=60, blank=False)

    def __str__(self) -> str:
        return f"Event: {self.title}"
