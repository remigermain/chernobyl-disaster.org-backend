from django.contrib import admin
from django.conf import settings
from utils.function import contenttypes_uuid
from utils.models import Issue, Commit


class AdminBase(admin.ModelAdmin):
    """
        model base for admin, with glocal function
    """
    empty_value_display = "- empty -"
    list_per_page = 20

    def langs_available(self, obj):
        return ", ".join(list(obj.langs.all().values_list('language', flat=True))) or self.empty_value_display

    def issue(self, obj):
        return Issue.objects.filter(uuid=contenttypes_uuid(obj)).count()

    def commit(self, obj):
        return Commit.objects.filter(uuid=contenttypes_uuid(obj)).count()


class AdminInlineBase(admin.TabularInline):
    def get_extra(self, request, obj=None, **kwargs):
        """
            return minimuin of language availables
        """
        _min = obj.langs.count() if obj else 1
        return min(_min, len(settings.LANGUAGES))
