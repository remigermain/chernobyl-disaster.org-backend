from django.test import TestCase, tag, RequestFactory
from timeline.models import Event, EventLang
from django.utils import timezone
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from timeline.serializer import EventSerializer, EventLangSerializer


@tag('models', 'event')
class EventTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.get_or_create(username="test", password="test")[0]
        self.request = RequestFactory()
        self.request.user = self.user

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

    @tag('serializer')
    def test_serializer_create(self):
        data = {
            'title': 'good',
            'date': timezone.now()
        }
        context = {'request': self.request}
        serializer = EventSerializer(data=data, context=context)

        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.date, data['date'])
        self.assertEqual(obj.title, data['title'])
        self.assertEqual(obj.creator, self.user)

    @tag('serializer')
    def test_serializer_update(self):
        self.test_create()
        event = Event.objects.first()
        self.assertEqual(event.contributors.count(), 0)

        data = {
            'title': event.title + '--test--',
        }
        context = {'request': self.request}
        serializer = EventSerializer(instance=event, data=data, context=context, partial=True)

        self.assertTrue(serializer.is_valid())
        obj = serializer.save()

        self.assertEqual(obj.id, event.id)
        self.assertEqual(obj.title, data['title'])
        self.assertEqual(obj.creator, self.user)
        self.assertIn(self.user, obj.contributors.all())

    @tag('serializer')
    def test_serializer_create_same_date(self):
        self.test_create()
        event = Event.objects.first()
        self.assertEqual(event.contributors.count(), 0)

        data = {
            'title': event.title + '--test--',
            'date': event.date
        }
        context = {'request': self.request}
        serializer = EventSerializer(data=data, context=context)

        self.assertFalse(serializer.is_valid())
        self.assertIsNotNone(serializer.errors['date'])

    @tag('serializer')
    def test_serializer_update_same_date(self):
        self.test_create()
        event = Event.objects.first()

        date = timezone.now()
        newevent = Event.objects.create(title="lalla", date=date, creator=self.user)
        self.assertIsNotNone(newevent.id)

        data = {
            'title': event.title + '--test--',
            'date': date
        }
        context = {'request': self.request}
        serializer = EventSerializer(instance=event, data=data, context=context)

        self.assertFalse(serializer.is_valid())
        self.assertIsNotNone(serializer.errors['date'])


@tag('models', 'event', 'lang')
class EventLangTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.get_or_create(username="test", password="test")[0]
        self.event = Event.objects.create(title='good', date=timezone.now(), creator=self.user)
        self.request = RequestFactory()
        self.request.user = self.user

    def test_create(self):
        lang = EventLang.objects.create(
            title="lallala",
            description="lalal",
            event=self.event,
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

    @tag('serializer')
    def test_serializer_create(self):
        self.test_create()
        data = {
            'title': 'title',
            'description': 'description',
            'event': self.event.pk,
            'language': 'fr'
        }
        context = {'request': self.request}
        serializer = EventLangSerializer(data=data, context=context)

        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.title, data['title'])
        self.assertEqual(obj.description, data['description'])
        self.assertEqual(obj.event.id, data['event'])
        self.assertEqual(obj.creator, self.user)

    @tag('serializer')
    def test_serializer_create_wrong_lang(self):
        self.test_create()
        data = {
            'title': 'title',
            'description': 'description',
            'event': self.event.pk,
            'language': 'frr'
        }
        context = {'request': self.request}
        serializer = EventLangSerializer(data=data, context=context)

        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_serializer_create_same_lang(self):
        self.test_create()
        data = {
            'title': 'title',
            'description': 'description',
            'event': self.event.pk,
            'language': EventLang.lang_default
        }
        context = {'request': self.request}
        serializer = EventLangSerializer(data=data, context=context)

        self.assertFalse(serializer.is_valid())
        self.assertIsNotNone(serializer.errors)

    @tag('serializer')
    def test_serializer_update(self):
        self.test_create()

        eventlang = EventLang.objects.first()
        data = {
            'title': eventlang.title + '--test--'
        }
        context = {'request': self.request}
        serializer = EventLangSerializer(instance=eventlang, data=data, context=context, partial=True)

        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNotNone(obj.title, data['title'])
        self.assertIn(self.user, obj.contributors.all())

    @tag('serializer')
    def test_serializer_update_wrong_lang(self):
        self.test_create()

        eventlang = EventLang.objects.first()
        data = {
            'title': eventlang.title + '--test--',
            'language': 'xx'
        }
        context = {'request': self.request}
        serializer = EventLangSerializer(instance=eventlang, data=data, context=context, partial=True)

        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_serializer_update_same_lang(self):
        self.test_create()
        event = EventLang.objects.first()

        new = EventLang.objects.create(title="tt", description="pp", creator=self.user, language="fr", event=self.event)
        self.assertIsNotNone(new.id)

        data = {
            'title': event.title + '--test--',
            'language': new.language
        }
        context = {'request': self.request}
        serializer = EventLangSerializer(instance=event, data=data, context=context, partial=True)

        self.assertFalse(serializer.is_valid())
