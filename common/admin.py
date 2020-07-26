from django.contrib import admin
from .models import Tag, TagLang, People, Issue, Commit
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


@admin.register(People)
class PeopleAdmin(AdminBase):
    list_display = ('name', 'pictures')

    def pictures(self, obj):
        return obj.pictures.count() if obj else 0
