from django.contrib import admin
from common.models import Tag, TagLang, Translate, TranslateLang
from lib.admin import AdminBase, AdminInlineBase


class TagLangInline(AdminInlineBase):
    model = TagLang


@admin.register(Tag)
class TagAdmin(AdminBase):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [
        TagLangInline
    ]


class TranslateLangInline(AdminInlineBase):
    model = TranslateLang


@admin.register(Translate)
class TranslateAdmin(AdminBase):
    list_display = ('key',)
    search_fields = ('key',)
    inlines = [
        TranslateLangInline
    ]
