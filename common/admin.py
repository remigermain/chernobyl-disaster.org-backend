from django.contrib import admin
from common.models import Tag, TagLang, Issue, Commit, Translate, TranslateLang
from lib.admin import AdminBase, AdminInlineBase


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'content_type', 'content_object', 'created')
    exclude = ('uuid',)


@admin.register(Commit)
class CommitAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'content_type', 'content_object', 'created')
    exclude = ('uuid',)


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
