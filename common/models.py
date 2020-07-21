from django.db import models


class Tag(models.Model):
    """
        tags pour tager les models, utile pour retrouver un photo d'une ville
        ou d'un evenement precis
    """

    name = models.CharField(max_length=50)


class Photographer(models.Model):
    """
        models pour regrouper les photos par photographes
    """
    name = models.CharField(max_length=80)
