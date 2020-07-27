from django.db import models
from lib.models import CreatorAbstract, LanguageAbstract
from django.core.exceptions import ValidationError


class EventExtraAbstract(CreatorAbstract):
    title = models.CharField(max_length=50)
    tags = models.ManyToManyField("common.Tag", related_name="%(class)s_extra", blank=True)
    event = models.ForeignKey("timeline.Event", on_delete=models.SET_NULL, null=True, related_name="%(class)ss")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.event} {self.__class__.__name__}"


def fnc_extra_path(instance, filename):
    """
        function to generate path file name
        ex: for Picture models as imagefiled named "my_pictures.png"
        the path is:
            50/Picture/10/my_pictures.png
    """
    return f"{instance.event.id}/{instance.__class__.__name__}/{filename}"


class Picture(EventExtraAbstract):
    image = models.ImageField(upload_to=fnc_extra_path)
    photographer = models.ForeignKey(
        "common.People",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pictures"
    )


class Document(EventExtraAbstract):
    image = models.ImageField(upload_to=fnc_extra_path, null=True, blank=True)
    doc = models.FileField(upload_to=fnc_extra_path, null=True, blank=True)

    def clean(self):
        # need to be one of image or doc set
        if self.image and self.doc:
            raise ValidationError("OneNotBoth")
        if not self.image and not self.doc:
            raise ValidationError("OneNotNothing")
        super().clean()


class Video(EventExtraAbstract):
    video = models.URLField()


class Article(EventExtraAbstract):
    link = models.URLField()


# Extra i18n

class EventExtraLangAbstract(LanguageAbstract):
    title = models.CharField(max_length=50, blank=True, null=True)

    get_parent_lang = 'extra'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['extra', 'language'], name="%(class)s_unique")
        ]
        abstract = True

    def __str__(self):
        return f"{self.extra} {self.language}"


class PictureLang(EventExtraLangAbstract):
    extra = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name="langs")


class DocumentLang(EventExtraLangAbstract):
    extra = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="langs")


class VideoLang(EventExtraLangAbstract):
    extra = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="langs")


class ArticleLang(EventExtraLangAbstract):
    extra = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="langs")


# Event Models

class Event(CreatorAbstract):
    """
        event models is a date event on chernobyl
        the title is for indication , tags for easy find here, and the date ...
        date is unnique , is not possible to have same date
    """
    title = models.CharField(max_length=100)
    tags = models.ManyToManyField('common.Tag', related_name="events", blank=True)
    date = models.DateTimeField(null=False, blank=False, unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date'], name="%(class)s_date_unique")
        ]

    def __str__(self):
        return f"{self.title} {self.date}"


class EventLang(LanguageAbstract):
    """
        models for i18n Event
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="langs")
    get_parent_lang = 'event'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['language', 'event'], name="%(class)s_unique")
        ]

    def __str__(self):
        return f"{self.event} {self.language}"
