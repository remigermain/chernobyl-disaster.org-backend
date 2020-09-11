from django.test import tag
from lib.test import BaseTest
from common.serializers.tag import TagSerializer


@tag('model', 'tag')
class TagTest(BaseTest):
    def test_create_serializer(self):
        data = {
            'name': 'test'
        }
        serialiser = TagSerializer(data=data, context=self.context)
        self.assertTrue(serialiser.is_valid())
        obj = serialiser.save()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.name, data['name'])
        self.check_creator(obj)
        return obj

    def test_create_serializer_update(self):
        obj = self.test_create_serializer()
        old_name = obj.name
        data = {
            'name': 'update-name'
        }

        serialiser = TagSerializer(instance=obj, data=data, context=self.context)
        self.assertTrue(serialiser.is_valid())
        updated = serialiser.save()
        self.assertEqual(updated.id, obj.id)
        self.assertNotEqual(updated.name, old_name)
        self.assertEqual(updated.name, data['name'])
        self.check_commit(updated)

    def test_create_serializer_empty(self):
        data = {}

        serialiser = TagSerializer(data=data, context=self.context)
        self.assertFalse(serialiser.is_valid())

    def test_create_serializer_same_name(self):
        obj = self.test_create_serializer()
        data = {
            'name': obj.name
        }

        serialiser = TagSerializer(data=data, context=self.context)
        self.assertFalse(serialiser.is_valid())

    @tag('serializer', 'langs')
    def test_create_serializer_langs(self):
        data = {
            'name': "name",
            'langs': [
                {
                    'name': 'test',
                    'language': self.lang
                }
            ]
        }

        serialiser = TagSerializer(data=data, context=self.context)
        self.assertTrue(serialiser.is_valid())
        obj = serialiser.save()
        self.assertEqual(obj.langs.count(), 1)
        self.assertEqual(obj.langs.first().name, data['langs'][0]['name'])
        self.check_creator(obj)

    @tag('serializer', 'langs')
    def test_create_serializer_empty_langs(self):
        data = {
            'name': "name",
            'langs': [
                {
                    'name': 'test'
                }
            ]
        }

        serialiser = TagSerializer(data=data, context=self.context)
        self.assertFalse(serialiser.is_valid())

    @tag('serializer', 'langs')
    def test_create_serializer_empty_langs(self):
        data = {
            'name': "name",
            'langs': [
                {
                    'name': 'test',
                    'language': self.lang
                },
                {
                    'name': 'test22',
                    'language': self.lang2
                }
            ]
        }

        serialiser = TagSerializer(data=data, context=self.context)
        self.assertTrue(serialiser.is_valid())
        obj = serialiser.save()
        self.assertEqual(obj.langs.count(), 2)
        self.assertEqual(obj.langs.first().name, data['langs'][0]['name'])
        self.assertEqual(obj.langs.first().language, data['langs'][0]['language'])
        self.assertEqual(obj.langs.last().name, data['langs'][1]['name'])
        self.assertEqual(obj.langs.last().language, data['langs'][1]['language'])
        self.check_creator(obj)