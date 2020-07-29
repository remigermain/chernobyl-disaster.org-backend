from django.test import tag
from lib.test import BaseTest
from common.models import Tag
from common.serializer import TagLangSerializer


@tag('model', 'tag', 'lang')
class TagLangTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.tag = Tag.objects.create(name='test', creator=self.user)

    @tag('serializer')
    def test_create_serializer(self):
        data = {
            'name': 'test',
            'tag': self.tag.pk,
            'language': self.lang
        }
        serialiser = TagLangSerializer(data=data, context=self.context)
        self.assertTrue(serialiser.is_valid())
        obj = serialiser.save()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.name, data['name'])
        self.assertEqual(obj.tag, self.tag)
        self.check_creator(obj)
        return obj

    @tag('serializer')
    def test_create_serializer_update(self):
        obj = self.test_create_serializer()
        old_name = obj.name
        old_language = obj.language
        data = {
            'name': 'update-name',
            'language': self.lang2
        }

        serialiser = TagLangSerializer(instance=obj, data=data, context=self.context, partial=True)
        self.assertTrue(serialiser.is_valid())
        updated = serialiser.save()
        self.assertEqual(updated.id, obj.id)
        self.assertNotEqual(updated.name, old_name)
        self.assertEqual(updated.name, data['name'])
        self.check_update_language(updated, old_language, data['language'])
        self.check_commit(updated)

    @tag('serializer')
    def test_create_serializer_update_wrong_lang(self):
        obj = self.test_create_serializer()
        data = {
            'language': 'testtest'
        }

        serialiser = TagLangSerializer(instance=obj, data=data, context=self.context, partial=True)
        self.assertFalse(serialiser.is_valid())

    @tag('serializer')
    def test_create_serializer_empty(self):
        data = {}

        serialiser = TagLangSerializer(data=data, context=self.context)
        self.assertFalse(serialiser.is_valid())
