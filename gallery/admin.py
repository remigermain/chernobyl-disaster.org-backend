from django.contrib import admin
from gallery.models import Character, CharacterLang, Video, VideoLang, Picture, PictureLang
from lib.admin import AdminBase, AdminInlineBase


class CharacterLangInline(AdminInlineBase):
    model = CharacterLang


@admin.register(Character)
class CharacterAdmin(AdminBase):
    list_display = ('id', 'name', 'langs_available', 'commit', 'issue')
    search_fields = ('id', 'name', 'born', 'death')
    inlines = [
        CharacterLangInline
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
