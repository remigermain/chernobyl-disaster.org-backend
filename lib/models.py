from django.db import models
from django.conf import settings
from utils.function import contenttypes_uuid
from lib.manager import QuerySetBase


class ChernobylModelAbstract(models.Model):
    """
        chernobyl base models
    """

    objects = QuerySetBase.as_manager()

    class Meta:
        abstract = True

    def to_url(self, field):
        link = getattr(self, field)
        if not link:
            return None
        link = link.url
        if not link[0] == "/":
            return f"{settings.SITE_URL}/{getattr(self, field).url}"
        return f"{settings.SITE_URL}{getattr(self, field).url}"

    def save(self, *args, **kwargs):
        # override the save for check every time the field
        if settings.DEBUG:
            self.full_clean()
        super(ChernobylModelAbstract, self).save(*args, **kwargs)
        return self

    def delete(self, *args, **kwargs):
        from utils.models import Commit
        uuid = contenttypes_uuid(self)
        ret = super().delete(*args, **kwargs)
        Commit.objects.filter(uuid=uuid).delete()
        return ret


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
        ordering = ['language']
