from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from lib.utils import contenttypes_uuid


class ChernobylModelAbstract(models.Model):
    """
        chernobyl base models
    """
    class Meta:
        abstract = True

    def get_issue(self):
        """
            return all issues on this models
        """
        from common.models import Issue
        return Issue.objects.filter(uuid=contenttypes_uuid(Issue, self))

    @property
    def issue_count(self):
        return self.get_issue().count()

    def get_commit(self):
        """
            return all commits from this models
        """
        from common.models import Commit
        return Commit.objects.filter(uuid=contenttypes_uuid(Commit, self))

    @property
    def commit_count(self):
        return self.get_commit().count()

    @property
    def updated(self):
        return self.get_commit().order_by('-created').first() or self.created

    def save(self, *args, **kwargs):
        # override the save for check every time the field
        self.full_clean()
        super(ChernobylModelAbstract, self).save(*args, **kwargs)
        return self


class CreatorAbstract(ChernobylModelAbstract):
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

    class Meta:
        abstract = True


class LogAbstract(CreatorAbstract):
    """
        models to repport or log every change
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    uuid = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self._meta.model_name} {self.creator} {self.uuid} {self.created}"

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.uuid = contenttypes_uuid(self, self.content_object)
        return super().save(*args, **kwargs)


class LanguageAbstract(CreatorAbstract):
    """
        models for internationalisation all content with
        language is small idetifation for lang ( ex :  french  are  fr )
    """
    lang_choices = settings.LANGUAGES
    lang_default = settings.LANGUAGES_DEFAULT

    language = models.CharField(choices=lang_choices, default=lang_default, max_length=4)

    class Meta:
        abstract = True
