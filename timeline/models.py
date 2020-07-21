from django.db import models
from core import settings


class EventAbstract(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    tags = models.ManyToManyField("commmon.Tag")
    event = models.ForeignKey("timeline.Event", on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class Picture(EventAbstract):
    image = models.ImageField()
    photographer = models.ForeignKey("common.Photographer", on_delete=models.SET_NULL, related_name="pictures")


class Document(EventAbstract):
    image = models.ImageField()


class Video(EventAbstract):
    link = models.URLField()


class Article(EventAbstract):
    link = models.URLField()


class LangEvent(models.Model):
    """
        description and title by languages for event
    """

    lang_choices = [lang[0] for lang in settings.LANGUAGES]
    lang_default = settings.LANGUAGES_DEFAULT

    language = models.CharField(choices=lang_choices, default=lang_default)
    title = models.CharField(max_length=100)
    description = models.TextField()
    event = models.ForeignKey('timeline.LangEvent', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('language', 'event')


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.ManyToManyField('common.Tag', related_name="events")
    date = models.DateTimeField(null=False, blank=False)
