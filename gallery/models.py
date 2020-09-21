from django.db import models
from lib.models import ChernobylModelAbstract, LanguageAbstract
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from timeline.models import EventExtraAbstract
from common.models import Tag


def uuid_path(instance, filename):
    """
        function to generate path file name
        ex: for Picture models as imagefiled named "my_pictures.png"
        the path is:
            50/Picture/10/my_pictures.png
    """
    return instance.pk if instance.pk else instance.__class__.objects.count() + 1


def picture_path(instance, filename):
    # get only filename , not path
    name = filename.split('/')[-1]
    return f"pictures/{uuid_path(instance, filename)}/{name}"


class Picture(EventExtraAbstract):
    picture = models.ImageField(upload_to=picture_path)
    picture_webp = ImageSpecField(source='picture', format='WEBP')
    picture_thumbnail_webp = ImageSpecField(source='picture',
                                            processors=[ResizeToFill(250, 160)],
                                            format='WEBP',
                                            options={'quality': 60})
    picture_thumbnail_jpeg = ImageSpecField(source='picture',
                                            processors=[ResizeToFill(250, 160)],
                                            format='JPEG',
                                            options={'quality': 60})

    photographer = models.ForeignKey(
        "gallery.People",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pictures"
    )


class Video(EventExtraAbstract):
    video = models.URLField(unique=True)


# Extra i18n
class EventExtraLangAbstract(LanguageAbstract):
    title = models.CharField(max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.extra} {self.language}"


class PictureLang(EventExtraLangAbstract):
    extra = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name="langs")


class VideoLang(EventExtraLangAbstract):
    extra = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="langs")


def profil_path(instance, filename):
    import re
    name = re.sub(r"[^a-zA-Z0-9]+", "", instance.name)
    extentions = filename.split('.')[-1]
    return f"people/{instance.id}/{name}.{extentions}"


class People(ChernobylModelAbstract):
    """
        models for personality of chernobyl
    """
    name = models.CharField(max_length=80, unique=True)
    born = models.DateField(null=True, blank=True)
    death = models.DateField(null=True, blank=True)
    profil = models.ImageField(upload_to=profil_path, null=True, blank=True)
    profil_webp = ImageSpecField(source='profil', format='WEBP')
    profil_thumbnail_webp = ImageSpecField(source='profil',
                                           processors=[ResizeToFill(250, 160)],
                                           format='WEBP',
                                           options={'quality': 60})
    profil_thumbnail_jpeg = ImageSpecField(source='profil',
                                           processors=[ResizeToFill(250, 160)],
                                           format='JPEG',
                                           options={'quality': 60})

    wikipedia = models.URLField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name="peoples", blank=True)

    def __str__(self):
        return self.name


class PeopleLang(LanguageAbstract):
    people = models.ForeignKey(People, on_delete=models.CASCADE, related_name="langs")
    biography = models.TextField()
