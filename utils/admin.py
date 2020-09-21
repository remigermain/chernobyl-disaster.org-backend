from django.contrib import admin
from utils.models import Issue, Commit, Contact


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'content_type', 'content_object', 'created')
    exclude = ('uuid',)


@admin.register(Commit)
class CommitAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'content_type', 'content_object', 'created')
    exclude = ('uuid',)

    def get_queryset(self, request):
        query = super().get_queryset(request)
        query.select_related('creator')
        return query


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass
