from django.db import models
from lib.models import CreatorAbstract, LanguageAbstract, LogAbstract


class Issue(LogAbstract):
    """
        model to report probleme on every models
    """
    message = models.TextField()


class Commit(LogAbstract):
    """
        model to commit all modification on every models
    """
    pass


class Tag(CreatorAbstract):
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
    get_parent_lang = 'tag'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['language', 'tag'], name="%(class)s_sunique")
        ]

    def __str__(self):
        return f"{self.name} {self.language}"


class People(CreatorAbstract):
    """
        models for personality of chernobyl
    """
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name
