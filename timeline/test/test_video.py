from django.test import TestCase, tag
from timeline.models import Video, VideoLang, Event
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


@tag('models', 'video')
class VideoTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.get_or_create(username="test", password="test")[0]
        self.event = Event.objects.create(title="test", creator=self.user, date=timezone.now())

    def test_create(self):
        obj = Video.objects.create(
            title="test",
            event=self.event,
            creator=self.user,
            video="https://test.fr"
            )
        self.assertIsNotNone(obj.id)

    def test_video(self):
        obj = Video(
            title="test",
            event=self.event,
            creator=self.user,
            video="wrong_link"
            )

        try:
            obj.save()
        except Exception as e:
            self.assertNotEqual(e, ValidationError)
            self.assertIsNotNone(e.error_dict['video'])


@tag('models', 'video', 'lang')
class VideoLangTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.get_or_create(username="test", password="test")[0]
        self.event = Event.objects.create(title="test", creator=self.user, date=timezone.now())
        self.video = Video.objects.create(
            title="test",
            event=self.event,
            creator=self.user,
            video="https://test.fr"
            )

    def test_create(self):
        obj = VideoLang.objects.create(
            title="test",
            creator=self.user,
            extra=self.video
            )
        self.assertIsNotNone(obj.id)
        self.assertIsNotNone(obj.language, VideoLang.lang_default)

    def test_same_lang(self):
        self.test_create()
        lang = VideoLang.objects.first()
        lang.id = None

        try:
            lang.save()
            self.assertIsNotNone(lang.id)
        except Exception as e:
            self.assertNotEqual(e, ValidationError)
            self.assertIsNotNone(e.error_dict['__all__'])

    def test_lang_not_exist(self):
        self.test_create()
        lang = VideoLang.objects.first()
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
        lang = VideoLang.objects.first()
        lang.id = None
        lang.language = "fr"

        lang.save()
        self.assertIsNotNone(lang.id)
        self.assertEqual(lang.language, "fr")
