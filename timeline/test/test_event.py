from django.test import TestCase, tag
from timeline.models import Event, EventLang
from django.utils import timezone
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


@tag('models', 'event')
class EventTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.get_or_create(username="test", password="test")[0]

    def test_create(self):
        date = timezone.now()
        event = Event.objects.create(title="good", date=date, creator=self.user)
        self.assertIsNotNone(event.id)

    def test_same_date(self):
        """
            check create event same date
        """
        self.test_create()
        event = Event.objects.first()
        event.id = None

        try:
            event.save()
            self.assertIsNotNone(event.id)
        except Exception as e:
            self.assertNotEqual(e, IntegrityError)


@tag('models', 'event', 'lang')
class EventLangTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.get_or_create(username="test", password="test")[0]

    def test_create(self):
        event = Event.objects.create(title='good', date=timezone.now(), creator=self.user)
        lang = EventLang.objects.create(
            title="lallala",
            description="lalal",
            event=event,
            creator=self.user
        )

        # check create
        self.assertIsNotNone(lang.id)
        # check language is default
        self.assertEqual(lang.language, EventLang.lang_default)

    def test_same_lang(self):
        self.test_create()
        lang = EventLang.objects.first()
        lang.id = None

        try:
            lang.save()
            self.assertIsNotNone(lang.id)
        except Exception as e:
            self.assertNotEqual(e, ValidationError)
            self.assertIsNotNone(e.error_dict['__all__'])

    def test_lang_not_exist(self):
        self.test_create()
        lang = EventLang.objects.first()
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
        lang = EventLang.objects.first()
        lang.id = None
        lang.language = "fr"

        lang.save()
        self.assertIsNotNone(lang.id)
        self.assertEqual(lang.language, "fr")
