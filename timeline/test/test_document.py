from django.test import TestCase, tag
from timeline.models import Document, DocumentLang, Event
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


@tag('models', 'document')
class DocumentTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.get_or_create(username="test", password="test")[0]
        self.event = Event.objects.create(title="test", creator=self.user, date=timezone.now())

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
