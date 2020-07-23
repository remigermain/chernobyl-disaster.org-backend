from django.test import TestCase, tag
from common.models import Tag, TagLang
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


@tag('models', 'tag')
class VideoTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.get_or_create(username="test", password="test")[0]

    def test_create(self):
        obj = Tag.objects.create(name="test", creator=self.user)
        self.assertIsNotNone(obj.id)


@tag('models', 'tag', 'lang')
class TagLangTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.get_or_create(username="test", password="test")[0]
        self.tag = Tag.objects.create(name="test", creator=self.user)

    def test_create(self):
        obj = TagLang.objects.create(
            name="test",
            creator=self.user,
            tag=self.tag
            )
        self.assertIsNotNone(obj.id)
        self.assertIsNotNone(obj.language, TagLang.lang_default)

    def test_same_lang(self):
        self.test_create()
        lang = TagLang.objects.first()
        lang.id = None

        try:
            lang.save()
            self.assertIsNotNone(lang.id)
        except Exception as e:
            self.assertNotEqual(e, ValidationError)
            self.assertIsNotNone(e.error_dict['__all__'])

    def test_lang_not_exist(self):
        self.test_create()
        lang = TagLang.objects.first()
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
        lang = TagLang.objects.first()
        lang.id = None
        lang.language = "fr"

        lang.save()
        self.assertIsNotNone(lang.id)
        self.assertEqual(lang.language, "fr")
