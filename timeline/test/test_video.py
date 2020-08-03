from django.test import tag
from timeline.models import Event
from timeline.serializers.video import VideoSerializer
from lib.test import BaseTest


@tag('model', 'video')
class VideoTest(BaseTest):
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
            'video': self.link
        }
        serializer = VideoSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.title, data['title'])
        self.assertEqual(obj.video, data['video'])
        self.assertEqual(obj.event.pk, data['event'])
        self.check_creator(obj)
        return obj

    @tag('serializer')
    def test_create_serializer_without_event(self):
        data = {
            'title': 'title',
            'video': self.link
        }
        serializer = VideoSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.title, data['title'])
        self.assertEqual(obj.video, data['video'])
        self.check_creator(obj)
        return obj

    @tag('serializer')
    def test_create_serializer_empty(self):
        data = {}

        serializer = VideoSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_wrong_event(self):
        data = {
            'title': 'title',
            'event': self.event.pk + 99,
            'video': self.link
        }
        serializer = VideoSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_same_link(self):
        obj = self.test_create_serializer()
        data = {
            'title': 'title',
            'event': obj.event.pk,
            'video': obj.video
        }
        serializer = VideoSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_update(self):
        obj = self.test_create_serializer()
        obj_id = obj.id
        obj_video = obj.video
        obj_title = obj.title
        data = {
            'title': 'update-title',
            'event': obj.event.pk,
            'video': self.link2
        }
        serializer = VideoSerializer(instance=obj, data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.id, obj_id)
        self.assertNotEqual(obj_video, obj.video)
        self.assertEqual(obj.video, data['video'])
        self.assertNotEqual(obj_title, obj.title)
        self.assertEqual(obj.title, data['title'])
        self.check_commit(obj)
