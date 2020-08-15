import os

from common.models import Tag
from timeline.models import Picture
from django.core.files import File
from django.contrib.auth import get_user_model


user = get_user_model().objects.get(username="remi")

title = "Duga radar"
tag = Tag.objects.get(name="Duga radar")

path = "/home/remi/Pictures/chernobyl/tour"



for f in os.listdir(path):
    name = os.path.join(path, f)
    if os.path.isfile(name):
        with open(name, 'rb') as file:
            p = Picture(title=title, picture=File(file), creator=user)
            p.save()
            p.tags.add(tag)
