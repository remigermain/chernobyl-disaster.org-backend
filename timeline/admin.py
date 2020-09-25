from django.contrib import admin
from .models import EventLang, Event
from lib.admin import AdminBase, AdminInlineBase


class EventLangInline(AdminInlineBase):
    model = EventLang


@admin.register(Event)
class EventAdmin(AdminBase):
    list_display = ('id', 'title', 'date', 'langs_available', 'commit', 'issue')
    search_fields = ('id', 'title', 'date')
    inlines = [
        EventLangInline
    ]
