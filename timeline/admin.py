from django.contrib import admin
from .models import Picture, Video, \
    PictureLang, VideoLang, EventLang, Event
from lib.admin import AdminBase, AdminInlineBase


class PictureLangInline(AdminInlineBase):
    model = PictureLang


@admin.register(Picture)
class PictureAdmin(AdminBase):
    list_display = ('picture', 'photographer')
    inlines = [
        PictureLangInline
    ]


class VideoLangInline(AdminInlineBase):
    model = VideoLang


@admin.register(Video)
class VideoAdmin(AdminBase):
    list_display = ('video', )
    inlines = [
        VideoLangInline
    ]


class EventLangInline(AdminInlineBase):
    model = EventLang


@admin.register(Event)
class EventAdmin(AdminBase):
    list_display = ('title', 'date')
    inlines = [
        EventLangInline
    ]
