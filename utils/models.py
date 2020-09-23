from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
from django.db import models
from utils.function import contenttypes_uuid


class CreatorAbstract(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    created = models.BooleanField(default=False)
    creator = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_creator"
    )

    class Meta:
        abstract = True
        ordering = ['-id']


class LogAbstract(CreatorAbstract):
    """
        models to repport or log every change
        uuid is the unique field , easy to filter by queryset
        uuid is define like :
        "Model_class | contenttype_app_label | contenttype_class | primarykey "
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    uuid = models.CharField(max_length=200)

    class Meta(CreatorAbstract.Meta):
        abstract = True

    def __str__(self):
        return f"{self._meta.model_name} {self.creator} {self.uuid} {self.created}"

    def save(self, *args, **kwargs):
        self.uuid = contenttypes_uuid(self.content_object)
        return super().save(*args, **kwargs)


class Issue(LogAbstract):
    """
        model to report probleme on every models
    """
    message = models.TextField()


class Commit(LogAbstract):
    """
        model to commit all modification on every models
    """
    updated_fields = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if isinstance(self.updated_fields, list):
            self.updated_fields = "|".join(self.updated_fields)
        return super().save(*args, **kwargs)


class Contact(CreatorAbstract):
    email = models.EmailField(null=False, blank=False)
    message = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"{self.creator} | {self.created}"
