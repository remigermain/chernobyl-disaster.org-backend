from django.db import models
from lib.models import CreatorAbstract, LanguageAbstract, LogAbstract
import re


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


def profil_path(instance, filename):
    name = re.sub(r"[^a-zA-Z0-9]+", "", instance.name)
    extentions = filename.split('.')[-1]
    return f"people/{instance.id}/{name}.{extentions}"


class People(CreatorAbstract):
    """
        models for personality of chernobyl
    """
    name = models.CharField(max_length=80, unique=True)
    born = models.DateField(null=True, blank=True)
    death = models.DateField(null=True, blank=True)
    profil = models.ImageField(upload_to=profil_path, null=True, blank=True)
    wikipedia = models.URLField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name="peoples", blank=True)

    def __str__(self):
        return self.name


class PeopleLang(LanguageAbstract):
    people = models.ForeignKey(People, on_delete=models.CASCADE, related_name="langs")
    biography = models.TextField()

    select_std = ['people']


class Contact(CreatorAbstract):
    message = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"{self.creator} | {self.created}"
