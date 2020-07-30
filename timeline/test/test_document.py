from django.test import tag
from django.core.files.uploadedfile import SimpleUploadedFile
from timeline.models import Event
from timeline.serializer import DocumentSerializer
from lib.test import BaseTest


@tag('model', 'document', 'test')
class DocumentTest(BaseTest):
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
            'doc': self.document
        }
        serializer = DocumentSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.title, data['title'])
        self.assertIsNotNone(obj.doc)
        self.assertEqual(obj.event.pk, data['event'])
        self.check_creator(obj)
        return obj

    @tag('serializer')
    def test_create_serializer_empty(self):
        data = {}

        serializer = DocumentSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_wrong_event(self):
        data = {
            'title': 'title',
            'event': self.event.pk + 99,
            'doc': self.document
        }
        serializer = DocumentSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_update(self):
        obj = self.test_create_serializer()
        obj_id = obj.id
        obj_video = obj.doc
        obj_title = obj.title
        data = {
            'title': 'update-title',
            'doc': self.document2
        }
        serializer = DocumentSerializer(instance=obj, data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.id, obj_id)
        self.assertNotEqual(obj_video, obj.doc)
        self.assertIsNotNone(obj.doc, data['doc'])
        self.assertNotEqual(obj_title, obj.title)
        self.assertEqual(obj.title, data['title'])
        self.check_commit(obj)
