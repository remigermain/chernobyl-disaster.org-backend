from django.test import tag
from timeline.models import Event
from timeline.serializers.picture import PictureSerializer
from lib.test import BaseTest


@tag('model', 'picture')
class PictureTest(BaseTest):
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
            'picture': self.picture
        }
        serializer = PictureSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.title, data['title'])
        self.assertIsNotNone(obj.picture)
        self.assertEqual(obj.event.pk, data['event'])
        self.check_creator(obj)
        return obj

    @tag('serializer')
    def test_create_serializer_without_event(self):
        data = {
            'title': 'title',
            'picture': self.picture
        }
        serializer = PictureSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.title, data['title'])
        self.assertIsNotNone(obj.picture)
        self.check_creator(obj)
        return obj

    @tag('serializer')
    def test_create_serializer_empty(self):
        data = {}

        serializer = PictureSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_wrong_event(self):
        data = {
            'title': 'title',
            'event': self.event.pk + 99,
            'picture': self.picture
        }
        serializer = PictureSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_update(self):
        obj = self.test_create_serializer()
        obj_id = obj.id
        obj_video = obj.picture
        obj_title = obj.title
        data = {
            'title': 'update-title',
            'picture': self.picture2
        }
        serializer = PictureSerializer(instance=obj, data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.id, obj_id)
        self.assertNotEqual(obj_video, obj.picture)
        self.assertIsNotNone(obj.picture, data['picture'])
        self.assertNotEqual(obj_title, obj.title)
        self.assertEqual(obj.title, data['title'])
        self.check_commit(obj)
