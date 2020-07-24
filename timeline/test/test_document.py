from django.test import TestCase, tag, RequestFactory
from timeline.models import Document, DocumentLang, Event
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from timeline.serializer import DocumentSerializer
from django.core.files.uploadedfile import SimpleUploadedFile


@tag('models', 'document')
class DocumentTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.get_or_create(username="test", password="test")[0]
        self.event = Event.objects.create(title="test", creator=self.user, date=timezone.now())
        self.request = RequestFactory()
        self.request.user = self.user
        self.file = SimpleUploadedFile('test', b"test")
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.image = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')

    def test_create(self):
        obj = Document.objects.create(
            title="test",
            event=self.event,
            creator=self.user,
            doc="test"
            )
        self.assertIsNotNone(obj.id)

        obj = Document.objects.create(
            title="test",
            event=self.event,
            creator=self.user,
            image="test"
            )
        self.assertIsNotNone(obj.id)

    def test_image_and_doc_set(self):
        obj = Document(
            title="test",
            event=self.event,
            creator=self.user,
            doc="test",
            image="test"
            )
        try:
            obj.save()
            self.assertIsNotNone(obj.id)
        except Exception as e:
            self.assertNotEqual(e, ValidationError)
            self.assertIsNotNone(e.error_dict['__all__'])

    def test_image_and_doc_noset(self):
        obj = Document(
            title="test",
            event=self.event,
            creator=self.user,
            )
        try:
            obj.save()
            self.assertIsNotNone(obj.id)
        except Exception as e:
            self.assertNotEqual(e, ValidationError)
            self.assertIsNotNone(e.error_dict['__all__'])

    @tag('serializer')
    def test_serializer_create(self):
        data = {
            'title': 'test',
            'event': self.event.pk,
            'doc': self.file
        }
        context = {'request': self.request}
        serializer = DocumentSerializer(data=data, context=context)

        # test with doc
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.title, data['title'])
        self.assertEqual(obj.event.pk, data['event'])

        data.pop('doc')
        data['image'] = self.image
        # test with image
        serializer = DocumentSerializer(data=data, context=context)

        serializer.is_valid()
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.title, data['title'])
        self.assertEqual(obj.event.pk, data['event'])

    @tag('serializer')
    def test_serializer_create_both(self):
        data = {
            'title': 'test',
            'event': self.event.pk,
            'doc': self.file,
            'image': self.file
        }
        context = {'request': self.request}
        serializer = DocumentSerializer(data=data, context=context)

        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_serializer_create_none(self):
        data = {
            'title': 'test',
            'event': self.event.pk,
        }
        context = {'request': self.request}
        serializer = DocumentSerializer(data=data, context=context)

        self.assertFalse(serializer.is_valid())


@tag('models', 'document', 'lang')
class DocumentLangTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.get_or_create(username="test", password="test")[0]
        self.event = Event.objects.create(title="test", creator=self.user, date=timezone.now())
        self.doc = Document.objects.create(
            title="test",
            event=self.event,
            creator=self.user,
            image="test"
            )

    def test_create(self):
        obj = DocumentLang.objects.create(
            title="test",
            creator=self.user,
            extra=self.doc
            )
        self.assertIsNotNone(obj.id)
        self.assertIsNotNone(obj.language, DocumentLang.lang_default)

    def test_same_lang(self):
        self.test_create()
        lang = DocumentLang.objects.first()
        lang.id = None

        try:
            lang.save()
            self.assertIsNotNone(lang.id)
        except Exception as e:
            self.assertNotEqual(e, ValidationError)
            self.assertIsNotNone(e.error_dict['__all__'])

    def test_lang_not_exist(self):
        self.test_create()
        lang = DocumentLang.objects.first()
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
        lang = DocumentLang.objects.first()
        lang.id = None
        lang.language = "fr"

        lang.save()
        self.assertIsNotNone(lang.id)
        self.assertEqual(lang.language, "fr")
