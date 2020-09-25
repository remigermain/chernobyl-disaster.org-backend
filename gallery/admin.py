from django.contrib import admin
from gallery.models import People, PeopleLang, Video, VideoLang, Picture, PictureLang
from lib.admin import AdminBase, AdminInlineBase


class PeopleLangInline(AdminInlineBase):
    model = PeopleLang


@admin.register(People)
class PeopleAdmin(AdminBase):
    list_display = ('id', 'name', 'langs_available', 'commit', 'issue')
    search_fields = ('id', 'name', 'born', 'death')
    inlines = [
        PeopleLangInline
    ]

    def pictures(self, obj):
        return obj.pictures.count() if obj else 0


class PictureLangInline(AdminInlineBase):
    model = PictureLang


@admin.register(Picture)
class PictureAdmin(AdminBase):
    list_display = ('id', 'title', 'langs_available', 'commit', 'issue')
    search_fields = ('id', 'title')
    inlines = [
        PictureLangInline
    ]


class VideoLangInline(AdminInlineBase):
    model = VideoLang


@admin.register(Video)
class VideoAdmin(AdminBase):
    list_display = ('id', 'title', 'langs_available', 'commit', 'issue')
    search_fields = ('id', 'title')
    inlines = [
        VideoLangInline
    ]
