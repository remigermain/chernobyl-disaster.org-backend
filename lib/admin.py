from django.contrib import admin
from django.conf import settings


class AdminBase(admin.ModelAdmin):
    """
        model base for admin, with glocal function
    """

    empty_value_display = "- empty -"

    def __init__(self, model, admin_site):

        __list_display = ('created', 'updated', 'issue_count', 'commit_count')
        __list_filter = ('created',)
        __search_fields = ('created',)

        # check if models have i18n field
        if hasattr(model, 'langs'):
            __list_display = ('langs_available',) + __list_display
            __list_filter = ('langs__language',) + __list_filter
            __search_fields = ('lang__language',) + __search_fields

        # assing default value
        self.list_display = ('id',) + self.list_display + __list_display
        self.list_filter = ('id',) + self.list_filter + __list_filter
        self.search_fields = ('id',) + self.search_fields + __search_fields

        super().__init__(model, admin_site)

    def langs_available(self, obj):
        lst = [obj['language'] for obj in obj.langs.values('language')]
        return " | ".join(lst) or None


class AdminInlineBase(admin.TabularInline):
    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        if obj:
            _count = obj.langs.count()
            return extra if len(settings.LANGUAGES) - _count != 0 else 1
        return extra