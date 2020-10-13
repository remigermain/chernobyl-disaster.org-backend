from django.db import models


class DateMixins(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    have_second = models.BooleanField(default=False)
    have_minute = models.BooleanField(default=False)
    have_hour = models.BooleanField(default=False)

    class Meta:
        abstract = True
