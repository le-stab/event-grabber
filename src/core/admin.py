from django.contrib import admin
from .models import Event, Speaker, TalkSession, Category

# Register your models here.
admin.site.register(Event)
admin.site.register(TalkSession)
admin.site.register(Speaker)
admin.site.register(Category)
