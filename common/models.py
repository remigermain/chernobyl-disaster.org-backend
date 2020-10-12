from django.db import models
from lib.models import ChernobylModelAbstract, LanguageAbstract
from django.contrib.auth import get_user_model


class Tag(ChernobylModelAbstract):
    """
        tags content for easy to find element by tag
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class TagLang(LanguageAbstract):
    """
        is only languages for tag name
    """
    name = models.CharField(max_length=50)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="langs")

    def __str__(self):
        return f"{self.name} {self.language}"

    @property
    def get_commit_id(self):
        return self.tag.id


class Translate(ChernobylModelAbstract):
    key = models.TextField(null=False, blank=True, unique=True)

    def __str__(self):
        return self.key


class TranslateLang(LanguageAbstract):
    value = models.TextField(null=False, blank=False)
    parent_key = models.ForeignKey(Translate, on_delete=models.CASCADE, related_name="langs", null=False)

    class Meta:
        ordering = ['-id']
        unique_together = ['parent_key', 'language']

    def __str__(self):
        return f"{self.get_language_display()}: {str(self.parent_key)}"

    @property
    def get_commit_id(self):
        return self.parent_key.id


class News(ChernobylModelAbstract):
    title = models.CharField(max_length=100, blank=False, null=False)
    text = models.TextField(blank=False, null=False)
    date = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=False)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_creator"
    )

    class Meta:
        ordering = ['-date', 'title']

    def __str__(self):
        return self.title
