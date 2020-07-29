from django.test import tag
from django.core.files.uploadedfile import SimpleUploadedFile
from timeline.models import Event, Picture
from timeline.serializer import PictureLangSerializer
from lib.test import BaseTest


@tag('model', 'picture', 'lang')
class PictureLangTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.event = Event.objects.create(
            title='good',
            date=self.time,
            creator=self.user
        )
        image = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.picture = SimpleUploadedFile('small.gif', image, content_type='image/gif')
        self.picture2 = SimpleUploadedFile('small2.gif', image, content_type='image/gif')
        self.extra = Picture.objects.create(
            title='title',
            event=self.event,
            picture=SimpleUploadedFile('base.gif', image, content_type='image/gif'),
            creator=self.user
        )

    @tag('serializer')
    def test_create_serializer(self):
        data = {
            'extra': self.extra.pk,
            'title': 'title',
            'language': self.lang
        }
        serializer = PictureLangSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.title, data['title'])
        self.assertEqual(obj.extra.pk, data['extra'])
        self.assertEqual(obj.language, data['language'])
        self.check_creator(obj)
        return obj

    @tag('serializer')
    def test_create_serializer_same_lang(self):
        obj = self.test_create_serializer()
        data = {
            'extra': self.extra.pk,
            'title': 'title',
            'language': obj.language
        }
        serializer = PictureLangSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_wrong_lang(self):
        data = {
            'extra': self.extra.pk,
            'title': 'title',
            'language': self.lang_wrong
        }
        serializer = PictureLangSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_empty(self):
        data = {}

        serializer = PictureLangSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_unk_extra(self):
        data = {
            'extra': self.extra.pk + 99,
            'title': 'title',
            'language': self.lang_wrong
        }
        serializer = PictureLangSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_update(self):
        obj = self.test_create_serializer()
        obj_id = obj.id
        obj_title = obj.title
        obj_language = obj.language
        data = {
            'title': 'update-title',
            'language': self.lang2
        }
        serializer = PictureLangSerializer(instance=obj, data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        updated = serializer.save()
        self.assertEqual(updated.id, obj_id)
        self.assertNotEqual(updated.title, obj_title)
        self.assertEqual(updated.title, data['title'])
        self.assertNotEqual(updated.language, obj_language)
        self.assertEqual(updated.language, data['language'])
        self.check_commit(updated)
