from django.db import models
from lib.models import CreatorAbstract, LanguageAbstract
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.template.defaultfilters import slugify


class EventExtraAbstract(CreatorAbstract):
    title = models.CharField(max_length=50)
    tags = models.ManyToManyField("common.Tag", related_name="%(class)s", blank=True)
    date = models.DateTimeField(blank=True, null=True)
    event = models.ForeignKey(
        "timeline.Event",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(class)ss"
    )

    select_std = ['event']

    class Meta:
        abstract = True

    def __str__(self):
        if self.event:
            return f"{self.event} {self.__class__.__name__} {self.title}"
        return f"{self.__class__.__name__} {self.title}"


def uuid_path(instance, filename):
    """
        function to generate path file name
        ex: for Picture models as imagefiled named "my_pictures.png"
        the path is:
            50/Picture/10/my_pictures.png
    """
    return instance.pk if instance.pk else instance.__class__.objects.count() + 1


def picture_path(instance, filename):
    return f"pictures/{uuid_path(instance, filename)}/{filename}"


def document_path(instance, filename):
    return f"document/{uuid_path(instance, filename)}/{filename}"


class Picture(EventExtraAbstract):
    picture = models.ImageField(upload_to=picture_path)
    picture_thumbnail = ImageSpecField(source='picture',
                                       processors=[ResizeToFill(250, 160)],
                                       format='WEBP',
                                       options={'quality': 60})

    photographer = models.ForeignKey(
        "common.People",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pictures"
    )
    select_std = EventExtraAbstract.select_std + ['photographer']


class Video(EventExtraAbstract):
    video = models.URLField(unique=True)

# Extra i18n

class EventExtraLangAbstract(LanguageAbstract):
    title = models.CharField(max_length=50)

    get_parent_lang = 'extra'
    select_std = ['extra']

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.extra} {self.language}"


class PictureLang(EventExtraLangAbstract):
    extra = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name="langs")


class VideoLang(EventExtraLangAbstract):
    extra = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="langs")


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
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return f"{self.title} {self.date}"

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

    get_parent_lang = 'event'
    select_std = ['event']

    def __str__(self):
        return f"{self.event} {self.language}"
