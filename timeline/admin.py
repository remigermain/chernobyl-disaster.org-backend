from django.contrib import admin
from .models import EventLang, Event
from lib.admin import AdminBase, AdminInlineBase


class EventLangInline(AdminInlineBase):
    model = EventLang


@admin.register(Event)
class EventAdmin(AdminBase):
    list_display = ('title', 'date')
    inlines = [
        EventLangInline
    ]
