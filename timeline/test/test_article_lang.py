from django.test import tag
from timeline.models import Event, Article
from timeline.serializer import ArticleLangSerializer
from lib.test import BaseTest


@tag('model', 'article', 'lang')
class ArticleLangTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.event = Event.objects.create(
            title='good',
            date=self.time,
            creator=self.user
        )
        self.extra = Article.objects.create(
            title='title',
            event=self.event,
            link=self.link,
            creator=self.user
        )

    @tag('serializer')
    def test_create_serializer(self):
        data = {
            'extra': self.extra.pk,
            'title': 'title',
            'language': self.lang
        }
        serializer = ArticleLangSerializer(data=data, context=self.context)
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
        serializer = ArticleLangSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_wrong_lang(self):
        data = {
            'extra': self.extra.pk,
            'title': 'title',
            'language': self.lang_wrong
        }
        serializer = ArticleLangSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_empty(self):
        data = {}

        serializer = ArticleLangSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_unk_extra(self):
        data = {
            'extra': self.extra.pk + 99,
            'title': 'title',
            'language': self.lang_wrong
        }
        serializer = ArticleLangSerializer(data=data, context=self.context)
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
        serializer = ArticleLangSerializer(instance=obj, data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        updated = serializer.save()
        self.assertEqual(updated.id, obj_id)
        self.assertNotEqual(updated.title, obj_title)
        self.assertEqual(updated.title, data['title'])
        self.assertNotEqual(updated.language, obj_language)
        self.assertEqual(updated.language, data['language'])
        self.check_commit(updated)
