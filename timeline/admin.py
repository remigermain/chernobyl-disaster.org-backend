from django.contrib import admin
from .models import Picture, Document, Video, Article, \
    PictureLang, DocumentLang, VideoLang, ArticleLang, EventLang, Event
from lib.admin import AdminBase, AdminInlineBase


class PictureLangInline(AdminInlineBase):
    model = PictureLang


@admin.register(Picture)
class PictureAdmin(AdminBase):
    list_display = ('picture', 'photographer')
    inlines = [
        PictureLangInline
    ]


class DocumentLangInline(AdminInlineBase):
    model = DocumentLang


@admin.register(Document)
class DocumentAdmin(AdminBase):
    list_display = ('doc',)
    inlines = [
        DocumentLangInline
    ]


class VideoLangInline(AdminInlineBase):
    model = VideoLang


@admin.register(Video)
class VideoAdmin(AdminBase):
    list_display = ('video', )
    inlines = [
        VideoLangInline
    ]


class ArticleLangInline(AdminInlineBase):
    model = ArticleLang

@admin.register(Article)
class ArticleAdmin(AdminBase):
    list_display = ('link', )
    inlines = [
        ArticleLangInline
    ]


class EventLangInline(AdminInlineBase):
    model = EventLang


@admin.register(Event)
class EventAdmin(AdminBase):
    list_display = ('title', 'date')
    inlines = [
        EventLangInline
    ]
