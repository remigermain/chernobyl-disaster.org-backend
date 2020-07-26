from django.contrib import admin
from .models import Tag, TagLang, People, Issue, Commit
from lib.admin import AdminBase, AdminInlineBase


class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'content_type', 'content_object', 'created')
    exclude = ('uuid',)


class CommitAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'content_type', 'content_object', 'created')
    exclude = ('uuid',)


class TagLangInline(AdminInlineBase):
    model = TagLang


class TagAdmin(AdminBase):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [
        TagLangInline
    ]


class PeopleAdmin(AdminBase):
    list_display = ('name', 'pictures')

    def pictures(self, obj):
        return obj.pictures.count() if obj else 0


admin.site.register(Issue, IssueAdmin)
admin.site.register(Commit, CommitAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(People, PeopleAdmin)
