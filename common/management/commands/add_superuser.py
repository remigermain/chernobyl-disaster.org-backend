from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = get_user_model().objects.filter(is_staff=True)
        _count = user.count()
        if _count == 1:
            user = user.first()
            print(f'user exist:\n\tusername: {user.username}')
        elif _count == 0:
            user = get_user_model().objects.create_superuser(username='a', password='a', email="a@a.a")
            user.save()
            print(f'user create:\n\tusername: {user.username}')
        else:
            print(f'Error, number on staf as {_count}')
