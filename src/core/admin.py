from django.contrib import admin
from django.utils.html import format_html
from .models import *

# Register your models here.
admin.site.register(Event)
admin.site.register(TalkSession)
admin.site.register(Category)
admin.site.register(EventTpl)


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    def img_tag(self, obj):
        return format_html('<img src="{}" width="80" />'.format(obj.img_url))
    img_tag.short_description = 'Image'
    list_display = ['id', 'img_tag','name']