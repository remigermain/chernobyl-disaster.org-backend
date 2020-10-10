from django.db import models
from lib.models import ChernobylModelAbstract, LanguageAbstract
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from timeline.models import EventExtraAbstract, EventExtraLangAbstract
from common.models import Tag
from lib.mixins.date import DateMixins
from django.template.defaultfilters import slugify


def primary_key_gen(instance):
    """
        function to generate path file name
        ex: for Picture models as imagefiled named "my_pictures.png"
        the path is:
            50/Picture/10/my_pictures.png
    """
    return str(instance.pk if instance.pk else instance.__class__.objects.count() + 1)


def name_files(title, filename):
    extentions = filename.split('.')[-1]
    return f"{slugify(title)}.{extentions}"


def picture_path(instance, filename):
    name = [
        instance.__class__.__name__.lower(),
        primary_key_gen(instance),
        name_files(instance.title, filename)
    ]
    return "/".join(name)


class Picture(DateMixins, EventExtraAbstract):
    date = models.DateTimeField(blank=True, null=True)

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

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title


class Video(DateMixins, EventExtraAbstract):
    date = models.DateTimeField(blank=True, null=True)

    video = models.URLField(unique=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title


class PictureLang(EventExtraLangAbstract):
    extra = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name="langs")


class VideoLang(EventExtraLangAbstract):
    extra = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="langs")


def profil_path(instance, filename):
    name = [
        instance.__class__.__name__.lower(),
        primary_key_gen(instance),
        name_files(instance.name, filename)
    ]
    return "/".join(name)


class People(ChernobylModelAbstract):
    """
        models for personality of chernobyl
    """
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
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

    tags = models.ManyToManyField(Tag, related_name="peoples", blank=True)

    def __str__(self):
        return self.name

    @property
    def tag_fields(self):
        return ['name']


class PeopleLang(LanguageAbstract):
    people = models.ForeignKey(People, on_delete=models.CASCADE, related_name="langs")
    biography = models.TextField()

    def __str__(self):
        return str(self.people)

    @property
    def get_commit_id(self):
        return self.people.id
