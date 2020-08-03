from django.test import tag
from lib.test import BaseTest
from timeline.models import Event
from timeline.serializers.event import EventLangSerializer


@tag('model', 'event', 'lang')
class EventLangTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.event = Event.objects.create(
            title='good',
            date=self.time,
            creator=self.user
        )

    @tag('serializer')
    def test_create_serializer(self):
        data = {
            'title': 'title',
            'description': 'description',
            'event': self.event.pk,
            'language': self.lang
        }
        serializer = EventLangSerializer(data=data, context=self.context)

        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.title, data['title'])
        self.assertEqual(obj.description, data['description'])
        self.assertEqual(obj.event.id, data['event'])
        self.check_creator(obj)
        return obj

    @tag('serializer')
    def test_serializer_create_wrong_lang(self):
        data = {
            'title': 'title',
            'description': 'description',
            'event': self.event.pk,
            'language': 'wrong'
        }
        serializer = EventLangSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_serializer_create_same_lang(self):
        obj = self.test_create_serializer()
        data = {
            'title': 'title',
            'description': 'description',
            'event': self.event.pk,
            'language': obj.language
        }
        serializer = EventLangSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_serializer_update(self):
        obj = self.test_create_serializer()
        event_id = obj.id
        event_title = obj.title
        event_lang = obj.language
        data = {
            'title': 'title-new',
            'language': self.lang2
        }
        serializer = EventLangSerializer(instance=obj, data=data, context=self.context, partial=True)

        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.id, event_id)
        self.assertNotEqual(obj.title, event_title)
        self.assertEqual(obj.title, data['title'])
        self.assertNotEqual(obj.language, event_lang)
        self.assertEqual(obj.language, data['language'])
        self.check_commit(obj)

    @tag('serializer')
    def test_serializer_update_wrong_lang(self):
        eventlang = self.test_create_serializer()
        data = {
            'title': 'title-new',
            'language': 'xx'
        }
        serializer = EventLangSerializer(instance=eventlang, data=data, context=self.context, partial=True)
        self.assertFalse(serializer.is_valid())
