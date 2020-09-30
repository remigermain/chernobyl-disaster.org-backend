from django.db import models
from lib.models import ChernobylModelAbstract, LanguageAbstract
from django.template.defaultfilters import slugify
from lib.mixins.date import DateMixins


class Event(DateMixins, ChernobylModelAbstract):
    """
        event models is a date event on chernobyl
        the title is for indication , tags for easy find here, and the date ...
        date is unnique , is not possible to have same date
    """
    slug = models.SlugField(max_length=100)
    title = models.CharField(max_length=100)
    tags = models.ManyToManyField('common.Tag', related_name="events", blank=True)
    date = models.DateTimeField(null=False, blank=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class EventLang(LanguageAbstract):
    """
        models for i18n Event
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="langs")

    def __str__(self):
        return f"{self.event} {self.language}"

    @property
    def get_commit_id(self):
        return self.event.id


class EventExtraAbstract(ChernobylModelAbstract):
    title = models.CharField(max_length=50)
    tags = models.ManyToManyField("common.Tag", related_name="%(class)s", blank=True)
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(class)ss"
    )

    class Meta(ChernobylModelAbstract.Meta):
        abstract = True


# Extra i18n
class EventExtraLangAbstract(LanguageAbstract):
    title = models.CharField(max_length=50)

    class Meta(LanguageAbstract.Meta):
        abstract = True

    def __str__(self):
        return f"{self.extra} {self.language}"

    @property
    def get_commit_id(self):
        return self.extra.id
