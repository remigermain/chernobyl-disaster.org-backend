from django.test import tag
from timeline.models import Event
from timeline.serializer import ArticleSerializer
from lib.test import BaseTest


@tag('model', 'article')
class ArticleTest(BaseTest):
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
            'event': self.event.pk,
            'link': self.link
        }
        serializer = ArticleSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.title, data['title'])
        self.assertEqual(obj.link, data['link'])
        self.assertEqual(obj.event.pk, data['event'])
        self.check_creator(obj)
        return obj

    @tag('serializer')
    def test_create_serializer_without_event(self):
        data = {
            'title': 'title',
            'link': self.link
        }
        serializer = ArticleSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.title, data['title'])
        self.assertEqual(obj.link, data['link'])
        self.check_creator(obj)
        return obj

    @tag('serializer')
    def test_create_serializer_empty(self):
        data = {}

        serializer = ArticleSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_wrong_event(self):
        data = {
            'title': 'title',
            'event': self.event.pk + 99,
            'link': self.link
        }
        serializer = ArticleSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_same_link(self):
        obj = self.test_create_serializer()
        data = {
            'title': 'title',
            'event': obj.event.pk,
            'link': obj.link
        }
        serializer = ArticleSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_update(self):
        obj = self.test_create_serializer()
        obj_id = obj.id
        obj_video = obj.link
        obj_title = obj.title
        data = {
            'title': 'update-title',
            'event': obj.event.pk,
            'link': self.link2
        }
        serializer = ArticleSerializer(instance=obj, data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.id, obj_id)
        self.assertNotEqual(obj_video, obj.link)
        self.assertEqual(obj.link, data['link'])
        self.assertNotEqual(obj_title, obj.title)
        self.assertEqual(obj.title, data['title'])
        self.check_commit(obj)
