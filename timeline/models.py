from django.db import models
from lib.models import ChernobylModelAbstract, LanguageAbstract
from django.template.defaultfilters import slugify


class Event(ChernobylModelAbstract):
    """
        event models is a date event on chernobyl
        the title is for indication , tags for easy find here, and the date ...
        date is unnique , is not possible to have same date
    """
    title = models.CharField(max_length=100)
    tags = models.ManyToManyField('common.Tag', related_name="events", blank=True)
    date = models.DateTimeField(null=False, blank=False, unique=True)
    slug = models.SlugField(max_length=100)

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


class EventExtraAbstract(ChernobylModelAbstract):
    title = models.CharField(max_length=50)
    tags = models.ManyToManyField("common.Tag", related_name="%(class)s", blank=True)
    date = models.DateTimeField(blank=True, null=True)
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(class)ss"
    )

    class Meta(ChernobylModelAbstract.Meta):
        abstract = True

    def __str__(self):
        if self.event:
            return f"{self.event} {self.__class__.__name__} {self.title}"
        return f"{self.__class__.__name__} {self.title}"
