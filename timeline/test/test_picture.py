from django.test import TestCase, tag
from timeline.models import Picture, PictureLang, Event
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


@tag('models', 'picture')
class PictureTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.get_or_create(username="test", password="test")[0]
        self.event = Event.objects.create(title="test", creator=self.user, date=timezone.now())

    def test_create(self):
        obj = Picture.objects.create(
            title="test",
            event=self.event,
            creator=self.user,
            image="test"
            )
        self.assertIsNotNone(obj.id)


@tag('models', 'picture', 'lang')
class PictureLangTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.get_or_create(username="test", password="test")[0]
        self.event = Event.objects.create(title="test", creator=self.user, date=timezone.now())
        self.image = Picture.objects.create(
            title="test",
            event=self.event,
            creator=self.user,
            image="test"
            )

    def test_create(self):
        obj = PictureLang.objects.create(
            title="test",
            creator=self.user,
            extra=self.image
            )
        self.assertIsNotNone(obj.id)
        self.assertIsNotNone(obj.language, PictureLang.lang_default)

    def test_same_lang(self):
        self.test_create()
        lang = PictureLang.objects.first()
        lang.id = None

        try:
            lang.save()
            self.assertIsNotNone(lang.id)
        except Exception as e:
            self.assertNotEqual(e, ValidationError)
            self.assertIsNotNone(e.error_dict['__all__'])

    def test_lang_not_exist(self):
        self.test_create()
        lang = PictureLang.objects.first()
        lang.id = None
        lang.language = "xx",

        try:
            lang.save()
            self.assertIsNotNone(lang.id)
        except Exception as e:
            self.assertNotEqual(e, ValidationError)
            self.assertIsNotNone(e.error_dict['language'])

    def test_new_lang(self):
        self.test_create()
        lang = PictureLang.objects.first()
        lang.id = None
        lang.language = "fr"

        lang.save()
        self.assertIsNotNone(lang.id)
        self.assertEqual(lang.language, "fr")
