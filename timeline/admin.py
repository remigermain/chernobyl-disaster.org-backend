from django.contrib import admin
from .models import Picture, Document, Video, Article, LangEvent, Event


class PictureAdmin(admin.ModelAdmin):
    list_display = ()
    list_filter = ()
    search_fields = ()


class DocumentAdmin(admin.ModelAdmin):
    list_display = ()
    list_filter = ()
    search_fields = ()


class VideoAdmin(admin.ModelAdmin):
    list_display = ()
    list_filter = ()
    search_fields = ()


class ArticleAdmin(admin.ModelAdmin):
    list_display = ()
    list_filter = ()
    search_fields = ()


class LangEventAdmin(admin.ModelAdmin):
    list_display = ()
    list_filter = ()
    search_fields = ()


class EventAdmin(admin.ModelAdmin):
    list_display = ()
    list_filter = ()
    search_fields = ()



admin.site.register(Picture, PictureAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(LangEvent, LangEventAdmin)
admin.site.register(Event, EventAdmin)
