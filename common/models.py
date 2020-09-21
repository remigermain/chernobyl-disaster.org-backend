from django.db import models
from lib.models import ChernobylModelAbstract, LanguageAbstract


class Tag(ChernobylModelAbstract):
    """
        tags content for easy to find element by tag
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class TagLang(LanguageAbstract):
    """
        is only languages for tag name
    """
    name = models.CharField(max_length=50)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="langs")
    get_parent_lang = 'tag'
    select_std = ['tag']

    def __str__(self):
        return f"{self.name} {self.language}"


class Translate(ChernobylModelAbstract):
    key = models.TextField(null=False, blank=True)

    def __str__(self):
        return self.key


class TranslateLang(LanguageAbstract):
    value = models.TextField(null=False, blank=False)
    parent_key = models.ForeignKey(Translate, on_delete=models.CASCADE, related_name="langs", null=False)
    select_std = ['parent_key']

    def __str__(self):
        return f"{self.parent_key}: {self.value}"
