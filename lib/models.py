from django.db import models
from django.conf import settings
from lib.manager import QuerySetBase


class ChernobylModelAbstract(models.Model):
    """
        chernobyl base models
    """

    objects = QuerySetBase.as_manager()

    class Meta:
        abstract = True
        ordering = ['-id']

    def save(self, *args, **kwargs):
        # override the save for check every time the field
        if settings.DEBUG:
            self.full_clean()
        super(ChernobylModelAbstract, self).save(*args, **kwargs)
        return self

    @property
    def get_commit_id(self):
        # need it for generate commit
        return self.id


class LanguageAbstract(ChernobylModelAbstract):
    """
        models for internationalisation all content with
        language is small idetifation for lang ( ex :  french  are  fr )
    """
    lang_choices = settings.LANGUAGES
    lang_default = settings.LANGUAGES_DEFAULT

    language = models.CharField(choices=lang_choices, max_length=4)

    class Meta:
        abstract = True
        ordering = ['language', '-id']


class DateAbstract(ChernobylModelAbstract):
    have_seconds = models.BooleanField(default=False)
    have_minutes = models.BooleanField(default=False)
    have_hours = models.BooleanField(default=False)

    class Meta(ChernobylModelAbstract.Meta):
        abstract = True
