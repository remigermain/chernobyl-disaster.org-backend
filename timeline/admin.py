from django.contrib import admin
from .models import Picture, Document, Video, Article, \
    PictureLang, DocumentLang, VideoLang, ArticleLang, EventLang, Event
from lib.admin import AdminBase, AdminInlineBase


class PictureLangInline(AdminInlineBase):
    model = PictureLang


class PictureAdmin(AdminBase):
    list_display = ('image', 'photographer')
    inlines = [
        PictureLangInline
    ]


class DocumentLangInline(AdminInlineBase):
    model = DocumentLang


class DocumentAdmin(AdminBase):
    list_display = ('image', 'doc')
    inlines = [
        DocumentLangInline
    ]


class VideoLangInline(AdminInlineBase):
    model = VideoLang


class VideoAdmin(AdminBase):
    list_display = ('video', )
    inlines = [
        VideoLangInline
    ]


class ArticleLangInline(AdminInlineBase):
    model = ArticleLang


class ArticleAdmin(AdminBase):
    list_display = ('link', )
    inlines = [
        ArticleLangInline
    ]


admin.site.register(Picture, PictureAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Article, ArticleAdmin)


class EventLangInline(AdminInlineBase):
    model = EventLang


class EventAdmin(AdminBase):
    list_display = ('title', 'date')
    inlines = [
        EventLangInline
    ]


admin.site.register(Event, EventAdmin)
