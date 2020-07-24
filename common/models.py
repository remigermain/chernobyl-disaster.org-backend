from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


class ChernobylModelBase(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # override the save for check every time the field
        self.full_clean()
        super(ChernobylModelBase, self).save(*args, **kwargs)
        return self


class ContributorAbstract(ChernobylModelBase):
    """
        creator is the original user would creat the models
        contributors is all user would modify/update the models
    """
    created = models.DateField(auto_now_add=True)
    creator = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_creator"
        )

    updated = models.DateField(auto_now=True)
    contributors = models.ManyToManyField(get_user_model(), related_name="%(class)s_contributor", blank=True)

    class Meta:
        abstract = True


class LanguageAbstract(ContributorAbstract):
    """
        models for internationalisation all content with
        language is small idetifation for lang ( ex :  french  are  fr )
    """
    lang_choices = settings.LANGUAGES
    lang_default = settings.LANGUAGES_DEFAULT

    language = models.CharField(choices=lang_choices, default=lang_default, max_length=4)

    class Meta:
        abstract = True


class Tag(ContributorAbstract):
    """
        tags content for easy to find element by tag
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class TagLang(LanguageAbstract):
    """
        is only languages for tag name
    """
    name = models.CharField(max_length=50)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="langs")
    get_parent_lang = 'tag'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['language', 'tag'], name="%(class)s_sunique")
        ]

    def __str__(self):
        return f"{self.name} {self.language}"


class People(ContributorAbstract):
    """
        models for personality of chernobyl
    """
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name
