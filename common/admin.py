from django.contrib import admin
from common.models import Tag, TagLang, Translate, TranslateLang, News
from lib.admin import AdminBase, AdminInlineBase
from django.contrib.auth import get_user_model
from django.db.models import Q


class TagLangInline(AdminInlineBase):
    model = TagLang


@admin.register(Tag)
class TagAdmin(AdminBase):
    list_display = ('name', 'langs_available', 'commit', 'issue')
    search_fields = ('name', )
    inlines = [
        TagLangInline
    ]


@admin.register(TranslateLang)
class TranslateLangAdmin(AdminBase):
    list_display = ('language', 'parent_key')
    search_fields = ('language', 'parent_key', 'value')


class TranslateLangInline(AdminInlineBase):
    model = TranslateLang


@admin.register(Translate)
class TranslateAdmin(AdminBase):
    list_display = ('key', 'langs_available', 'commit', 'issue')
    search_fields = ('key',)
    inlines = [
        TranslateLangInline
    ]


@admin.register(News)
class NewsAdmin(AdminBase):
    list_display = ('id', 'title', 'date', 'author', 'is_active')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['author'].queryset = get_user_model().objects.filter(Q(is_staff=True) | Q(is_superuser=True))
        return form
